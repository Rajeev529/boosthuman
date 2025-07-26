from django.http import JsonResponse
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

# Load environment variables once when the application starts
load_dotenv()

# Set environment variables from .env file
os.environ['LANGCHAIN_API_KEY'] = os.getenv('langapi')
os.environ['GOOGLE_API_KEY'] = os.getenv('gemapi')
os.environ['LANGCHAIN_TRACING_V2'] = 'true'

# Initialize LLM and prompt template once
llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash', temperature=0.7)
output_parser = StrOutputParser()
prompt_template = PromptTemplate(
    input_variables=["link", "msg"],
    template="Visit URL {link} and provide a concise summary of the content(in 2 line with easy language english) based on the user's message: {msg}"
)

# Create the chain outside the function
chain = prompt_template | llm | output_parser

def chatbot(request):
    """
    A Django view function that uses a LangChain to interact with a Gemini LLM.
    """
    # 1. Get parameters safely, providing a default value.
    link = request.GET.get('link')
    msg = request.GET.get('msg')

    # 2. Basic validation: check if parameters exist.
    if not link or not msg:
        return JsonResponse({"error": "Missing 'link' or 'msg' parameters."}, status=400)

    try:
        # 3. Invoke the chain with validated and sanitized data.
        # (For production, you would add more robust sanitization/validation)
        response = chain.invoke({'link': link, 'msg': msg})
        
        # 4. Return a successful response.
        return JsonResponse({"status": response})
    
    except Exception as e:
        # 5. Handle potential errors gracefully.
        
        return JsonResponse({"error": "An internal server error occurred."}, status=500)