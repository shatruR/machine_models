# LangChain OpenAI Summarization

This project uses the LangChain framework with OpenAI's GPT-3.5-turbo model to generate summaries of given texts. The primary goal is to experiment with and learn from the code by running it locally and understanding its components.

## Features

- Generates a summary of a given text based on a user-defined question.
- Uses LangChain's prompt templates and output parsers.
- Environment variable management using `dotenv`.

## Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/langchain-openai-summarization.git
    cd langchain-openai-summarization
    ```

2. **Create a virtual environment and activate it:**

    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Create a `.env` file in the root directory and add your API keys:**

    ```plaintext
    OPENAI_API_KEY=your_openai_api_key
    LANGCHAIN_API_KEY=your_langchain_api_key
    ```

## Usage

1. **Run the summarization script:**

    ```sh
    python summarize.py
    ```

2. **Example code snippet:**

    ```python
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser

    import os
    from dotenv import load_dotenv

    # Load environment variables from a .env file
    load_dotenv()

    # Set environment variables for OpenAI and LangChain API keys
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

    # Create a chat prompt template with a system message and user message
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant. Please respond to the user request only based on the given context."),
            ("user", "Question: {question}\nContext: {context}")
        ]
    )

    # Initialize the OpenAI chat model
    model = ChatOpenAI(model='gpt-3.5-turbo')

    # Create an output parser to parse the output as a string
    output_parser = StrOutputParser()

    # Create a chain of operations: prompt -> model -> output parser
    chain = prompt | model | output_parser

    # Define the question and context
    question = "Can you summarize the speech in less than 30 words?"
    context = """
    Even though you are only a very small speck of ocean, of the 300 million children on whose shoulders the future of India rests, you can ignite the minds, light the fire, become a burning candle to light another candle. My dear children, you work in the school for about 25000 hours before you complete 12th std. Within the school curriculum / school hours, I want you to contribute to the Mission of Developed India by involving in the student centric activities like Literacy Development, Eco-Care Movement.

    India after its independence was determined to move ahead with planned policies for Science & Technology. Now, India is very near to self-sufficiency in food, making the ship to mouth existence of 1950s, an event of the past. Also improvements in the health sector, have eliminated few contagious diseases. There is a increase in life expectancy. Small scale industries provide high percentage of National GDP - a vast change in 1990s compared to 1950s. Today India can design, develop and launch world class geo-stationary and sun synchronous, remote sensing satellites.

    The nuclear establishments have reached the capability of building nuclear power stations, nuclear medicine and nuclear irradiation of agricultural seeds for growth in agricultural production. Today India has become a Nuclear Weapon State. Defence Research had led to design, development and production of Main Battle Tanks, strategic missile systems, electronic warfare systems and various armours. India is a missile power. Also we have seen growth in the Information Technology; the country is progressing in hardware and software export business of more than 10 billion dollars even though there are low ebbs in the last few years. India yet is a developing country. What Technology can do further?

    Technology has multiple dimensions. Geopolitics convert the technology to a particular nation's policy. The same policy will lead to economic prosperity and capability for national security. For example, the developments in chemical engineering brought fertilizers for higher yield of crops while the same science led to chemical weapons. Likewise, rocket technology developed for atmospheric research helped in launching satellites for remote sensing and communication applications which are vital for the economic development. The same technology led to development of missiles with specific defense needs that provides security for the nation. The aviation technology development has led to fighter and bomber aircraft, and the same technology will lead to passenger jet and also help operations requiring quick reach of support to people affected by disasters. At this stage, let us study global growth of technology and impact in human life.
    """

    # Invoke the chain with the question and context
    response = chain.invoke({"question": question, "context": context})

    # Print the response
    print(response)
    ```

## Notes

- This project is based on another user's project and has been adapted for personal learning and experimentation.
- Ensure that you do not expose your API keys in any public repository or share them with unauthorized users.

## License

[MIT](LICENSE)

