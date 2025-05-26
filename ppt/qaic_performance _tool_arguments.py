review.qualcomm.com / qranium / aic_perf / refs/heads/master / . / performance / llm_code / src / tools / qaic_performance / tool_arguments.py
blob: 7bc75d2a95429eb95d350c6b64a4dbc3ce53cc68 [file] [log] [blame] [edit]
import os
import re
from llm_code.src.constants import Constants as const
import sys
from loguru import logger
from subprocess import Popen, PIPE
from llm_code.src.utils.command_executor import CommandExecutor
class ToolArguments:
    '''
        Module which can fetch all the arguments to be used for input and output args
    '''
    def __init__(self,command : str,help_flag : bool = True, separator : str = "    " , re_pattern : str = ""):
        '''
            Initializer Function which will expect the below arguments
            Args:
                command (str)    : Tool whose arguments to be fetched
                help_flag (bool) : Flag to add --help in the command
                separator (str)  : separator to split the arguments and the description
                re_pattern (str) : regex patter to fetch the exact arguments
        '''
        self.command = command
        self.help_flag = help_flag
        self.separator = separator
        self.re_pattern = re_pattern
        self.run_command = CommandExecutor()
    def get_arguments(self):
        '''
            Method to get all the arguments of a tool/app.
            Return:
                args (list) : list of arguments for a tool/app
        '''
        #print("STAGE 1 : Getting a data for a tool/app --help section")
        raw_command_response = self.get_command_data()
        if not raw_command_response:
            logger.exception("command execution to fetch the help description is failed. please check logs")
            return []
        #print("STAGE 2 : Getting a flags with description removed")
        raw_args = self.get_flags_remov_desc(raw_command_response,separator = self.separator)
        #print("STAGE 3 : Getting a exact Args using a regex parsing")
        args = self.parse_args(raw_args,self.re_pattern)
        return args
    
    def get_command_data(self):
        '''
            Function to generate the response of a command
            Return:
                response (str) : returns the response of the command
        '''
        if self.help_flag:
            command = self.command + " --help"
        response,code = self.run_command.execute(command)
        #print(response)
        if code:
            logger.error(f"Error occured while executing the command resp {response}")
            return False
        return response
    def get_flags_remov_desc(self , data: str, separator : str = "") -> list:
        '''
            Method to remove the description in the arguments
            Args:
                data (str)      : command response whose description to be removed
                separator (str) : string to used as a separator
            Return:
                args (list) : list of arguments with removal of description
        '''
        args = []
        # splitting the data line baseds
        splitted_data = data.split("\n")
        for arg in splitted_data:
            args.append(arg.split(separator)[0])
        return args
    def parse_args(self,data :list,pattern : str) -> list :
        '''
            Method to parse the exact arguments based on the regex pattern
            Args:
                data (str)      : command response whose description to be removed
                pattern (str)   : regex pattern to exactly parse the argument
            Return:
                args (list) : list of arguments
        '''
        args = []
        for arg in data:
            matches = re.findall(pattern, arg)
            args.extend(matches)
        args = self.remove_duplicates_elements(args)
        return args
    def remove_duplicates_elements(self,data : list) -> list:
        '''
            Method to remove duplicate occurence in a list
            Args:
                data (list)   : list of arguments whose duplicate entries to be removed
            Return:
                duplicated_removed_data (list) : list of arguments with duplicates removed
        '''
        duplicated_removed_data = list(set(data))
        return duplicated_removed_data
