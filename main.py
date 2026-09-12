from utils.llm import get_llm

def main():
    llm=get_llm()
    response=llm.invoke("Reply with exactly: gemini connected succesfully")
    print(response.content)

if __name__ == "__main__":
    main()
