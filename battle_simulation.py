from huggingface_hub import login
from dotenv import load_dotenv
import os
import random
from typing import List
from langchain import LLMChain
from langchain.llms import OpenAI
from langchain import PromptTemplate
import json
from crit_numbers import critical_hit_numbers, training, find_victor

load_dotenv()

def battle_simulation(Player1: str, Player2: str) -> str:

    with open('battle_data.json', 'r') as f:
        stats = json.load(f)
   
    Player1Type = stats[Player1]['Type']
    Player2Type = stats[Player2]['Type']
    Player1CritNumber = stats[Player1]['CritNumber']

    Player2CritNumber = stats[Player2]['CritNumber']

    CritNumber = critical_hit_numbers(1)
    Player1CritNumbers = critical_hit_numbers(Player1CritNumber)
    Player2CritNumbers = critical_hit_numbers(Player2CritNumber)
    

    if (CritNumber in Player1CritNumbers) and (CritNumber not in Player2CritNumbers):

        template = """

        You oversee a battle between two skilled fighers. 
        The first fighter is {Player1} ({Player1Type}), while the second is 
        {Player2} ({Player2Type}). 
        You must decide which fighter will ultimately emerge victorious. 
        Create their abilities and use knowledge of magical spell's strengths 
        and weaknesses to determine the outcome of this epic showdown. 
        Simulate and describe the battle in just two sentences and decide who wins. 
        This time, {Player1} deals a critical hit! 
        Describe the fight and declare 'The victor is: '. 
        """

    elif (CritNumber not in Player1CritNumbers) and (CritNumber in Player2CritNumbers):


        template = """

        You oversee a battle between two skilled fighers. 
        The first fighter is {Player1} ({Player1Type}), while the second is 
        {Player2} ({Player2Type}). 
        You must decide which fighter will ultimately emerge victorious. 
        Create their abilities and use knowledge of magical spell's strengths 
        and weaknesses to determine the outcome of this epic showdown. 
        Simulate and describe the battle in just two sentences and decide who wins. 
        This time, {Player2} deals a critical hit! 
        Describe the fight and declare 'The victor is: '. 
        """

    else:
        template = """

        You oversee a battle between two skilled fighers. 
        The first fighter is {Player1} ({Player1Type}), while the second is 
        {Player2} ({Player2Type}). 
        You must decide which fighter will ultimately emerge victorious. 
        Create their abilities and use knowledge of magical spell's strengths 
        and weaknesses to determine the outcome of this epic showdown. 
        Simulate the battle in just two sentences and decide who wins. 
        Always end declaring 'The victor is: '
        """

    prompt = PromptTemplate(
            template=template,
            input_variables=["Player1", "Player2", "Player1Type", "Player2Type"]
            )
    # initialize Hub LLM
    #hub_llm = HuggingFaceHub(
    #        repo_id='google/flan-t5-xl',
    #    model_kwargs={'temperature':1e-10}
    #)

    llm = OpenAI(temperature=0.9)


    # create prompt template > LLM chain
    llm_chain = LLMChain(
        prompt=prompt,
        llm=llm
    )

    try:
        response = llm_chain.run({
                                    "Player1": Player1, 
                                    "Player2": Player2, 
                                    "Player1Type": Player1Type,
                                    "Player2Type": Player2Type
                                })
        
        victor = find_victor(response)

        if victor in stats.keys():
            stats[victor]['Wins']+=1
            stats[victor]['CritNumber']+=10
            with open('battle_data.json', 'w') as f:
                json.dump(stats, f)

            return response
    
    except Excepton as e:
        print(e)
def fair_fight_decider(PlayerClass: str) -> bool:
    """Decide whether the chosen class is fair."""
    template = """

    You are oversee fantasy fights and decide whether a character is beatable by a regular class like Mage or Knight. 
    I will describe a character class. Respond with True if this class is realistically beatable and false if not. 
    The class is {PlayerClass}. Respond only true or false.

    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["PlayerClass"]
        )
    
    llm = OpenAI(temperature=0.9)

    llm_chain = LLMChain(
        prompt=prompt,
        llm=llm
    )

    try:
        response = llm_chain.run(PlayerClass)
        victor = response.rstrip('.')
        return bool(victor)
    except Excepton as e:
        Exception('There was an error.', e)