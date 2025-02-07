
import argparse
import os
import tempfile
import time
from typing import Dict

from silagent.build.loader import BuildLoader
from silagent.container.base import Result
from silagent.core.collector import Collector
from silagent.core.error import LoadError
from silagent.core.fs import FileSystem, get_silagent_root

from silagent.core.yaml import load_yaml
from silagent.runner.engine import BaseRunnerEngine
from silagent.runner.factory import RunnerEngineFactory
from silagent.tests.base import BaseCommand
from silagent.tests.factory import CommandFactory
from silagent.tests.loader import CommandsLoader

def execute_from_command_line ():
    parser = argparse.ArgumentParser()
    parser.add_argument( "path" )

    args = parser.parse_args()

    fs = FileSystem( args.path )

    with fs.open( "siltest.yaml", "r" ) as file:
        text = file.read()
        yaml = load_yaml(text)

    print("Building images...")
    builder = BuildLoader.load(fs, yaml)
    builder.build()

    prefix = get_silagent_root().abspath + os.sep
    
    with tempfile.TemporaryDirectory( prefix = prefix ) as temp:
        collect_fs = FileSystem(temp)

        volume_fs = collect_fs.subdir( "volume" )
        os.mkdir( volume_fs.abspath )

        print()
        print("Collecting commands... ", end="")
        commands_collector = CommandsLoader.load( fs, yaml["tests"] )
        commands_collector.collect( volume_fs )
        
        commands: Dict[str, BaseCommand] = {}
        for cname, cfs in commands_collector.collected:
            with cfs.open("command.yaml", "r") as file:
                cyml = load_yaml( file.read() )
            commands[cname] = CommandFactory.create_command( cname, **cyml )
        print("OK")

        runner_fs = collect_fs.subdir( "runner" )
        os.mkdir( runner_fs.abspath )

        print("Collecting runners... ", end="")
        runner_collector = Collector()
        runner_collector.add_to_collection( fs.subdir("runner"), "runner" )
        runner_collector.collect( runner_fs )
        print("OK")

        print("Preparing runners... ", end="")

        runner_engines: "Dict[str, BaseRunnerEngine]" = {}
        for name, rfs in runner_collector.collected:
            engine, yaml = RunnerEngineFactory.find_runner_engine( name, rfs )

            engine.prepare( volume_fs, **yaml )

            runner_engines[name] = engine
        
        print("OK")

        print()

        tests_fs = fs.subdir("tests")

        print("Running tests...")

        had_failure = 0

        for test_file in tests_fs.listdir():
            print(f"  Running {test_file}...", end="")

            with tests_fs.open( test_file, "r" ) as file:
                test_yaml = load_yaml( file.read() )
            
            if "runner" not in test_yaml:
                raise LoadError('test.runner', 'The "runner" field does not exist in the test yaml')
            runner = test_yaml["runner"]
            engine = runner_engines.get( runner )
            if engine is None:
                raise LoadError('test.runner', f'Could not find the runner {runner}')
            
            if "steps" not in test_yaml:
                raise LoadError('test.steps', 'The "steps" field does not exist in the test yaml')
            steps = test_yaml["steps"]
            if not isinstance(steps, list):
                raise LoadError('test.steps', 'The "steps" field should be a list')
            
            targets = engine.names
            for step in steps:
                if not isinstance(step, dict):
                    raise LoadError('test.steps', "Each step should be a dict")
                if "target" not in step:
                    raise LoadError('test.steps', 'Each step should have a "target"')
                if step["target"] not in targets:
                    raise LoadError('test.steps', 'Invalid target : ' + step["target"] + " for the runner " + runner)
                if "args" not in step:
                    raise LoadError('test.steps', 'Each step should have a "args"')
                if not isinstance(step["args"], list) or any( list(map(lambda x : not isinstance(x, str), step["args"])) ):
                    raise LoadError('test.steps', 'The "args" of each step should be an array of strings')
                if "command" not in step:
                    raise LoadError('test.steps', 'Each step should have a "command"')
                if step["command"] not in commands:
                    raise LoadError('test.steps', 'Invalid command : ' + step["command"])
            
            containers = engine.run()
            containers_by_name = {}
            for container in containers:
                containers_by_name[ container.name ] = container
            
            valid = True
            for index, step in enumerate(steps):
                container = containers_by_name[ step["target"] ]
                command   = commands[ step["command"] ]
                args      = step["args"]

                step_result: Result = command.execute( container, args )
                
                if step_result.exit_code != 0:
                    print("FAILED on step", index + 1)
                    print()
                    print(step_result.output)
                    print()
                    valid = False
                    had_failure = True
                    break
            
            if valid:
                print("OK")
            engine.close()

        if had_failure: exit(1)