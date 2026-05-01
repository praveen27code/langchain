from langchain_ollama import OllamaLLM
import wikipedia
import re

def wiki_search(query: str) -> str:
    """Search Wikipedia for general knowledge"""
    try:
        return wikipedia.summary(query, sentences=2)
    except:
        return "No results found"

def create_llm():
    llm = OllamaLLM(model="mistral")
    return llm #return llm instance

def run_agent(llm, user_query: str):
    """Simple agent that decides when to search Wikipedia and add two numbers"""

    if( "add" in user_query.lower() or "sum" in user_query.lower()):
        # Extract numbers from the query
        numbers = re.findall(r'\d+', user_query)
        if len(numbers) >= 2:
            a, b = int(numbers[0]), int(numbers[1])
            return add(a, b)
        else:
            return "Please provide two numbers to add."
    
    # First, ask the LLM if it needs to search Wikipedia
    decide_prompt = f'You are a helpful assistant. The user asked: "{user_query}"\n\nDo you need to search Wikipedia to answer this question? Answer with ONLY "YES" or "NO".'
    
    decision = llm.invoke(decide_prompt).strip().upper()
    
    if "YES" in decision:
        # Extract potential search terms from the query
        search_prompt = f'Extract a single search term from this user query for Wikipedia: "{user_query}"\nRespond with ONLY the search term, nothing else.'
        print("\nDeciding to search Wikipedia...")
        search_term = llm.invoke(search_prompt).strip()
        wiki_result = wiki_search(search_term)
        
        # Generate final answer using the Wikipedia content
        final_prompt = f'Based on this Wikipedia information: "{wiki_result}"\nAnswer the user\'s question: "{user_query}"\nKeep the answer concise and helpful.'
        
        response = llm.invoke(final_prompt)
    else:
        # If no search needed, just answer directly
        final_prompt = f'Answer this question concisely: "{user_query}"'
        response = llm.invoke(final_prompt)
    
    return response

def add(a: int, b: int) -> int: 
    """A simple addition tool"""
    return a + b

def main():
    llm = create_llm()
    query = input("Ask something: ")
    response = run_agent(llm, query)
    print("\nAnswer:", response)

if __name__ == "__main__":
    main()