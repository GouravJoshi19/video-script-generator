from langchain.llms import Cohere
from langchain.prompts import ChatPromptTemplate
import streamlit as st


cohere_api_key = st.secrets.api_keys.cohere_api_key


cohere_llm=Cohere(cohere_api_key=cohere_api_key,
           model="command-xlarge-nightly",
           temperature=0.7,
           )

system_template_1="you are a user who has to provide an honest and personlized reviews about a product by looking at the details."
system_template_3="you are a social media expert you have come across a succesful instagram reel i want you to analyze this reel using the {reels_details} to understand what makes it sucessful,and then draft a new reel for our product with the help of the {product_review} the new reel should be different from the post you have analyzed.You can take inspiration from the analyzed reel but be original and create a new angle also don't start with a welcome jump straight into topic by providing only the title and the script as a plain text"

prompt_1=ChatPromptTemplate([
    ('system',system_template_1),('user','{product_details}')
])


prompt_2=ChatPromptTemplate([
  ('system',system_template_3),('user','{reels_details}{product_review}')
])


class LLM:
  def generate_review(self,user_input):
    formatted_prompt=prompt_1.format(product_details=user_input)
    Response=cohere_llm(formatted_prompt)
    return Response

  def generate_script(self,details,review):
    formatted_input=prompt_2.format(reels_details=details,product_review=review)
    response=cohere_llm(formatted_input)
    return response
  

  
def main():
  llm=LLM()
  description=["64MP front and rear camera","8GB RAM","snapdragon x elite processor","6.5inch oled display"]
  details=" Galti Sivi Kaviri Laplaud, Madkana Bina Aichi Stryker Chaat GPD mejake Type karo, Create a 7-day Instagram Reels Content Calendar With Engaging Real Ideas, Taylor to my niche Each Reels should aim to inspire, educate or entertain while subtly showcasing whatever your product or services The content should resonate with the enter target audience here And support my goal of growing followers, building brand authority or boosting sales Ensure each Reel includes a catchy hook, a clear call to action and suggested visuals Present everything in a table format Comment Prompt and I will send this from to you"

  review=llm.generate_review(description)
  script=llm.generate_script(details,review)

  file_name='script.txt'
  with open(file_name, "w", encoding="utf-8") as file:
      file.write(script)
if __name__=="__main__":
  main()