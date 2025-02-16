import json
def get_current_temperature(location: str, unit: str = "celsius"):
    """Get current temperature at a location.

    Args:
        location: The location to get the temperature for, in the format "City, State, Country".
        unit: The unit to return the temperature in. Defaults to "celsius". (choices: ["celsius", "fahrenheit"])

    Returns:
        the temperature, the location, and the unit in a dict
    """
    return {
        "temperature": 26.1,
        "location": location,
        "unit": unit,
    }


def get_temperature_date(location: str, date: str, unit: str = "celsius"):
    """Get temperature at a location and date.

    Args:
        location: The location to get the temperature for, in the format "City, State, Country".
        date: The date to get the temperature for, in the format "Year-Month-Day".
        unit: The unit to return the temperature in. Defaults to "celsius". (choices: ["celsius", "fahrenheit"])

    Returns:
        the temperature, the location, the date and the unit in a dict
    """
    return {
        "temperature": 25.9,
        "location": location,
        "date": date,
        "unit": unit,
    }


i = 3
def counter():
    global i
    i = i + 1
    print("counter program:" + str(i))
    return i

def reset_counter():
    global i
    i = 0
    print("counter reset:" + str(i))
    return i

def executeFunction(functionString: str,returnValueName :str):
    try:
        resultDict = {}
        exec(functionString,resultDict)
        return resultDict[returnValueName]

    except Exception as e:
        print(e)
        return False



def get_function_by_name(name):
    if name == "get_current_temperature":
        return get_current_temperature
    if name == "get_temperature_date":
        return get_temperature_date

    if name == "counter":
        return counter
    if name == "reset_counter":
        return reset_counter

    if name == "executeFunction":
        return executeFunction


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_temperature",
            "description": "Get current temperature at a location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": 'The location to get the temperature for, in the format "City, State, Country".',
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": 'The unit to return the temperature in. Defaults to "celsius".',
                    },
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_temperature_date",
            "description": "Get temperature at a location and date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": 'The location to get the temperature for, in the format "City, State, Country".',
                    },
                    "date": {
                        "type": "string",
                        "description": 'The date to get the temperature for, in the format "Year-Month-Day".',
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": 'The unit to return the temperature in. Defaults to "celsius".',
                    },
                },
                "required": ["location", "date"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "counter",
            "description": "Add 1 to the counter and get current number, only one is added each time, if you want add "
                           "more than one times, call multiple times",
        },
    },
    {
        "type": "function",
        "function": {
            "name": "reset_counter",
            "description": "Reset the counter and get current number",
        },
    },
    {
        "type": "function",
        "function": {
            "name": "executeFunction",
            "description": "you can input a python program and the computer will execute the function and the result "
                           "will be return to you in a dictionary. There should not be any return in the function, you "
                           "are also able to know one of the value in the program, pass that as the second parameter."
                           "use ; to separate each line, do not use '\n'",
            "parameters": {
                "type": "object",
                "properties": {
                    "functionString": {
                        "type": "string",
                        "description": 'The function to execute, and should be executable. You should input the entire '
                                       'function with no arguments. ',
                    },
                    "returnValueName": {
                        "type": "string",
                        "description": 'The value you want to know, will exact same name as in the executable program',
                    },
                },
                "required": ["functionString"],
            },
        },
    },
]
MESSAGES = [
    {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant.\n\nCurrent Date: 2024-09-30"},
]