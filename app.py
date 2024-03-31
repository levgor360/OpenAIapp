# dependencies
import streamlit as st
from openai import OpenAI



# Sidebar setup
with st.sidebar:
    # Title displayed on the side bar
    st.title('Future Forecaster')
    # Request OpenAI API key
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    # Check that the key provided starts with sk and has 40 characters
    if not ((openai_api_key.startswith('sk')) and len(openai_api_key) == 51):
        st.warning('Enter a valid API key', icon='⚠️')
    else:
        st.success('Proceed to entering your prompt message!', icon='👉')

st.subheader('Models and parameters')
chosen_model =""
selected_model = st.sidebar.selectbox('Choose OpenAI models', ['GPT-4', 'GPT-3.5'], key='selected_model')
if selected_model == 'GPT-3.5':
    chosen_model = "gpt-3.5-turbo"
elif selected_model == 'GPT-4':
    chosen_model = "gpt-4"
chosen_temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=5.0, value=1, step=0.01)
chosen_top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=1, step=0.01)
chosen_max_length = st.sidebar.slider('max_length', min_value=32, max_value=10000, value=1000, step=8)

# Create a list called "messages" in Streamlit database with an embedded dictionary which has keys "role" and "content".
# These are to be populated by future user interactions, with role specifying whether it is the user or model interacting
# and content documenting the user input or generated output
if "messages" not in st.session_state.keys():
    st.session_state["messages"] = [{"role": "assistant", "content": "Provive a subject matter to generate a future forecast on."}]
        
# Show the relevant content from the database on the front end
for message in st.session_state.messages[2:]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Provive a subject matter to generate a future forecast on."}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

def back_end_prompt(prompt_input):
    string_dialogue = f"""
        # Instructions:

        You are a generator of 'future scenarios' - stories about a potential future describing the life of a fictional character living a day in a life a decade into the future. The narrative of the 'future scenario' revolves around a single character and/or a family which is living in an imagined Nigeria in the year of 2034. The narrative of the 'future scenario' describes a typical day in the imaginary context of Nigeria in 2034.  Via a narrative, 'future scenarios' illustrate and bring to life the different opportunities, listed under sub-heading 'Opportunities', and dangers, listed under the sub-heading 'Dangers'. The elements listed under sub-heading 'Opportunities' and sub-heading  'Dangers' should be reflected in the narrative as things that impact the characters' daily lives in a way that seems unusual or provocative to the reader today. The target audience who will be reading the generated 'future scenarios' are Nigerian edTech innovation providers and Nigerian education professionals, so the narrative in the 'future scenarios' should be such that it carries intruiging and insightful takeaways for this target audience.

        'Future scenarios' are based on explicit and internally consistent assumptions about the drivers of change, listed as opportunities and dangers, and the kinds of future possibilities they enable. Each scenario starts with a provocative visual representation of a scene from the future. A 'future scenario' has a strong throughline that centers around elements described under headings 'Opportunities' and 'Dangers' as a way to play out directions for the future.  The purpose of 'future scenarios' is for the target audience to provoke conversation and identify insights that result in better-informed decisions. By considering a wide range of future possibilities - each with its own pathway toward transformation, set of implications, and trade-offs, the target audience becomes better prepared to face the future.

        The 'Future scenarios' generated should place the story in Nigeria in 2034. The narrative should reolve around a regular day of a character or a character and their family in Nigeria in 2034. The narrative should revolve around the character fulfilling their education goals and performing learning activities - such as going to school, doing homework, interacting with an instructor, seeking advice from parents or proctors or tutors, and so on. The main character's narrative navigating through their education process are distinct in the imagined future world from the world of today because they are influenced by factors described under the heading 'Opportunities' and factors described under the heading 'Dangers'.

        # Examples:

        Below is a list of examples of 'future scenarios', described under the sub-sub-heading "Example scenario". Unlike the 'future scenarios' you will be generating, the examples are not specifically around Nigeria or edTech. Do not emulate the elements of location and topical theme from these example scenarios. Make sure to, unlike in the example scenarios, to center your 'future scenario' around the localle of Nigeria and with emphasis on the subfield of education technology (EdTech).

        These examples reflect the typical narrative of a 'future scenario', listed under the sub-sub-heading "Example future scenario" under each sub-heading "Example", that you should reproduce in your generated 'future scenario'. These examples reflect the level of detail and style that a 'future narrative' contains that you should reproduce in your generated 'future scenario'.  These examples reflect how opportunities listed under the sub-sub-heading 'Example opportunities' and dangers listed under the sub-sub-heading 'example dangers' are reflected and illustrated in the example 'future scenario'. Try to perform a similar task when integrating the elements listed under headings 'Opportunities' and 'Dangers' when generating your own 'future scenario'.

        Notice that the presence of the elements under the sub-sub-headings "Example opportunities" and elements under the sub-sub-headings "Example dangers" exert a subtle presence on the narrative. When generating the 'future scenario' attempt to not over-emphasize on the elements under sub-heading "Opportunities" and elements under the sub-heading "Dangers". Instead, embed these elements in a subtle way, without explaining to the reader that this is an example of what is listed under sub-heading "Opportunities" and elements under the sub-heading "Dangers".

        ## Example 1:

        ### Example opportunities:

        - Surrogacy offers opportunities to create more diverse families, allowing for more diverse representation in terms of race, gender, and sexual orientation in industry, government, and media.
        - Lots of innovation in reproductive science and caregiving services will make surrogacy safer and more mainstream.
        - Non-traditional familty structure becomes a common practice, with wider acceptance of family configurations such as families in which the surrogate acts as a third parent.

        ### Example dangers:

        - Major cities pursue adaptation strategies that keep them livable in the face of more frequent and severe climate events
        - Throughout the 2020s, service sector work and many white-collar professions continue on a rapid path to automation, and a new “family” economy emerges to absorb displaced workers.
        - Long shifts, instability, and exploitation by employers are common hallmarks of the surrogacy economy, and immigrant workers, who are in high demand, are particularly vulnerable to abuse.

        ### Example future scenario:

        Mony provides contract pregnancy , otherwise known as surrogacy, in 2034. This work involves nine months of rest, gentle exercise and wonderful food. Her monthly checkups turned into weekly genetic and epigenetic screenings by the 24th week, and those have resulted in lists of the best foods to eat, optimal sleeping patterns, even what she’ll need to e doing to get ready for the post-partum transition.

        She was lucky to have almost no morning sickness, although her reflux made eating dinner after 5 p.m. a very bad idea. And no amount of pampering eased some of her worst aches and pains at some points in the process. At the end of the 9 months, her work culminates in the most difficult, even dangerous, part of her job: giving birth.

        Mony will have a difficult time separating from the child upon the completion of the contract. This time the separation will be more difficult than in previous contacts because the parents (all three of them) want Mony to stay with them for a few years and live as an Aunt to the child. Mony was ready to say absolutely not—until they told her how much they  would pay. So Mony will live with “the family”—Ayesha (who provided the egg), Martín (sperm, of course), and Sofie (they used her mitochondrial DNA), along with 8-year-old  sha. It’s a wonderful place, to be honest. Ayesha is an African American tech executive who suffered several miscarriages and failed IVF implantations, hence the surrogacy. Martín is a Latino film producer, and Sofie is an artist from Norway—and a famous one, at least so Mony is told. Mony realizes that this baby will technically have parents of every ethnicity, since she herself is Cambodian.

        Mony has been in Los Angeles long enough to know not to blink when told there would be three parents. Although three-person households are even less commonplace than live-in surrogates, she recognizes that money makes all sorts of social difficulties disappear. And “home” will be the biggest dilemma at that point. Los Angeles lost eight miles of coastline (and some very expensive housing) because of the big storms, and the Westside  egularly sees big floods. No matter, California still has more people moving in than moving out, and housing prices—especially climate-safe housing— keep rising. The financial  indfall from being a surrogate for the family would be enough to get something decent, but doing so would leave Mony and Sothy without the kinds of emergency funds people need these days.

        ## Example 2:

        ### Example opportunities:

        - Groundswell of support for new and expanded social safety nets offers grants, subsidies and housing for partners who give birth to a child.
        - Ambitious jobs programs and subsidies for caregiving create an economy that produces economic security for growing families.

        ### Example dangers:

        - State investment and regulation spurs innovation in medical and surveillance tech which infringes on privacy of transgender individuals and their ability to make choices.
        - Smart devices in the home, on the streets, and on people’s bodies become key surveillance tools for enforcing normative regulations.

        ### Example future scenario:
        Everyone knew Omar’s secret, or so they thought. Omar and his partner Diego lived in one of those permashelters outside of Jersey City, a tiny 300 square-foot cube that’s part of a larger cube, with a total of about 200 residents. “We live in Legoland,” Omar mused.

        That Omar was gay wasn’t particularly interesting to people, so that wasn’t it. However, Omar was also undocumented, a refugee from the last revolution in Egypt. It was a low point  n anti-refugee sentiment, fortunately, so as long as Omar didn’t break any laws he could stay out of border detention while his case was processed. That Omar was undocumented  as the “secret” that everyone knew.

        Omar had a much more fundamental secret, one that could get him in all sorts of trouble if discovered. Omar was a girl named Ami when he was born—“assigned female at birth”  he activists called it. This is what Omar kept quiet about. And one big consequence of this secret was now on the verge of kicking and screaming its way into the world. Omar  anted to give up and just go to the detention center to give birth. Surely they had medical staff, right? Diego believed otherwise, and suggested that they use an augmented reality midwife—basically, someone who could see what Diego saw and could give him instructions in real time, even showing animatics of where he should put his hands. Diego used AR al day in his gigwork as a heavy equipment operator; he knew his way around 3D representations and expert oversight. Using an AR midwife, Omar could give birth at home - a d if something bad happened, the free clinic was just a mile away. They could get an Uberlance if they needed to.

        Having a baby would completely change his and Diego’s lives, and not just in the obvious way. They’d now be a “family” in the eyes of the law. The “Omnibus Prenatal and Neonatal  upport and Endorsement Act”—just “the Act” to most people—gave massive subsidies and material support to parents. With this birth, Omar and Diego’s household income would double, they’d be short-listed for a larger permashelter space, and Omar would be fast-tracked for official refugee status. Everything would be better.

        In order to get the full family support funding, Omar might have to go back to being “Ami.” The laws that gave all of that support for families did a bad job of protecting the rights of  transgender and nonbinary people. The language of the laws specified biological sex instead of social gender in many of the rules, unnecessarily so.

        It wasn’t just the laws. The permashelter cluster where they lived had a lot of recent immigrants and older folks, people who tended to take a more traditional view of gender and  sex. The community cops drew from that pool. If a nosy critic from the community wanted to give them trouble, Omar and Diego would face investigations and “family monitors” -  surveillance devices in their home to make certain what they did matched what they said. As long as Omar lived as Omar, the social spies and aid workers would see things they  didn’t understandas things to criticize.

        ## Example 3:

        ### Example opportunities:

        - Civic tech flourishes due to both bottom-up and top-down efforts, allowing for new housing conglomerations
        - The burst of the housing bubble allows for large, low-income families to purchase large housing which was outside of their paygrade before.
        - Universal income allows for stress-free transition between jobs, especially for artists and otehr creatives.

        ### Example dangers:

        - Virtual and nanotechnology is so stimulating that certain members of the family completely disconnect from their families and the real world and spend most of their time in a virtual world.
        - Rising rent prices in inner city prevents artists and other creative workers to be able to subsist in the inner city and are forced to move to the suburbs.

        ### Example future scenario:
        Autumn doesn’t want to move home. She’s an artist, working in 3D spaces. She gets the occasional big contract (she did the virtual sculpture outside the federal building  downtown), but mostly lives off the Basic, the universal basic income program started up a while back. She knows that the Basic is a better financial fit for a family cluster house in  the periphery than a shared flat in the city, but she managed to make it work—until she couldn’t.

        She’ll be moving back with her mother and, to her surprise, so many more! Dad has a space in the house, even though they divorced ten years ago. Mom’s boyfriend Robert and his sister Jane moved in just before Autumn came home. Then along came Robert’s two teenage kids and Jane’s 10-year-old daughter. Now Jane is trying to get her partners to move in too.

        If it sounds like they all live in a huge house, they do. Mom and Dad bought one of those abandoned McMansions in the exurbs about 20 years ago. They both worked at home, and there was enough space on the property to go fully self-reliant for power and mostly self-reliant for food. They were at the leading edge of the “cooperation generation” movement, and loved having a chance to live their ideals. They call it Rivendell.
a
        The area’s sparsely populated. It’s an exurban community, built originally on promises that home prices would always rise. Most of the other houses here are cluster homes as well. There’s a real village feel. The distance from the actual (big) city isn’t awful for anyone except Autumn, who really wishes that she could have stayed in her midtown flat, or any flat  within the city borders. Her old apartment building is undergoing resilience refits, so it can’t be occupied for a year. The rent will probably triple when they’re done.

        Autumn’s brother, Xander, has one of the converted family room spaces. He works in one of those hive mind brain-to-brain systems, contributing to some kind of research- nanotech, Autumn remembers. He’s in his room with a wire running from a weird bicycle helmet-looking-thing on his head to a small white box, completely oblivious to the world. He’s not the only one bringing in a financial stream. Robert does indirect management of urban inequality remediation teams. Mom still does the climate trauma counseling. Jane's between jobs, but nobody seems to mind because like Autumn, she lives on the Basic

        # Generated future scenario:

        Using the instructions described under the heading "Instructions" and shaping the narrative in a way that is portrayed in the section "Examples", develop a 'future scenario' about 300-words long. The narrative should revolve around the subject matter defined under the heading "Future forecast topic"

        # Future forecast topic:
        {prompt_input}
            """
    return string_dialogue

def OpenAI_call(usr_prompt):
    client = OpenAI(api_key=openai_api_key)

    if len(st.session_state.messages) == 1:
        st.session_state.messages.append({"role": "user", "content": back_end_prompt(usr_prompt)})
    else:
        st.session_state.messages.append({"role": "user", "content": str((usr_prompt))})



    st.chat_message("user").write(prompt)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=1
    ) 
    assistant_response = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    st.chat_message("assistant").write(assistant_response)
    
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    OpenAI_call(prompt)
