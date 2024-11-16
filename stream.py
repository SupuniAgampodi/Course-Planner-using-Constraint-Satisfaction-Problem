import streamlit as st
import subprocess

# Define custom CSS styles with background image and additional styling
page_by_img = """
<style>
[data-testid="stAppViewContainer"]
{
    background-image: url("data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBw0QDw8SEBAPDRAPDw8NDQ8PDxsPDw8PFREWFhUVFRUYKCggGBolGxUTITEhJSkrLi4uFx8zODMsNygtLisBCgoKBQUFDgUFDisZExkrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrK//AABEIAL4BCgMBIgACEQEDEQH/xAAXAAEBAQEAAAAAAAAAAAAAAAAAAQIF/8QAGxABAQEAAwEBAAAAAAAAAAAAAAECE1KSEVH/xAAWAQEBAQAAAAAAAAAAAAAAAAAAAgH/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwDk8uu2vVOXXbXqsCmN8uu2vVOXXbXqsAN8uu2vVOXXbXqsL8Brl1216py67a9VgBvl1216py67a9VgBvl1216py67a9Vj6A3y67a9U5ddteqwA3y67a9U5ddteqwA3y67a9U5ddteqx8Ab5ddteqcuu2vVYAb5ddteqcuu2vVYPoN8uu2vVOXXbXqsAN8uu2vVOXXbXqsAN8uu2vVOXXbXqsL8Brl1216py67a9VgBvl1216py67a9VgBvl1216py67a9Vj6AAAAQGpEtLUAAAS1SAQAAABZEi2gWoAAAJasIAAAAAuYWlqAAAJapIBAAAAAgAAAC2ggAAAAEAAAAAFtQAAAAAJAAAAFtBAAAAAAAABKsAAABZAQW1AAAASgoSAAAAshaCAAAACWrIAAACyAg1ayAAAUAAAAAItqAAAAABIAAAAALagAAAAASAAAALb+IAAALEAKAAAAQAAAAAItQAAAAAgAAAAALUAAAAAAAAAAAAAAWQtBAAAS0FCQAAABZAQW1AAABLVkAAAAAFkLQQAAEtBRJFAAAIALagAAAEAAAAACLagAAAABAAAAAAW1AAAAJAAAAAAgAAAC2oAAAAAEAAAAAFtQAAAAAIAAAAtqAAAAAAAAFBKsPgAAAsiRbQLUAAABKqSAsgAAALIWrayAAAABUkJFAAAWRGrfwC1kAAWAgUAAAAgAAAAARaCAAAABAAAAAAWoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD//Z");
    background-size: cover;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

.content {
    padding: 20px;
    color: black;
    position: relative;
    z-index: 1;
    text-align: center;
}

.title {
    font-size: 36px;
    color: black; /* Changed title color to black */
    margin-bottom: 30px;
}

.logo {
    position: absolute; /* Position the logo absolutely */
    top: 10px; /* Distance from the top */
    right: 10px; /* Distance from the right */
    width: 100px; /* Adjust the width as needed */
    height: auto; /* Maintain aspect ratio */
}

.button {
    background-color: #4CAF50;
    border: none;
    color: black; /* Changed button text color to black */
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 10px;
    cursor: pointer;
    border-radius: 12px;
    transition-duration: 0.4s;
}

.button:hover {
    background-color: #45a049;
}

.text-input {
    background-color: rgba(255, 255, 255, 0.5);
    border: none;
    border-radius: 12px;
    padding: 15px 20px;
    margin-bottom: 20px;
    color: black; /* Added to set text color to black */
}

.text-input:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(70, 130, 180, 0.5);
}
</style>
"""

st.markdown(page_by_img, unsafe_allow_html=True)


def run_app(course_code):
    try:
        output = subprocess.check_output(['python', 'app.py', course_code]).decode('utf-8')
        st.markdown(f'<div class="output-container">{output}</div>', unsafe_allow_html=True)
    except subprocess.CalledProcessError as e:
        st.error(f'Error: {e}')


def main():
    st.markdown('<div class="content">', unsafe_allow_html=True)
    # Add the logo image to the top-right corner
    st.image("https://seekvectorlogo.com/wp-content/uploads/2021/11/murdoch-university-vector-logo-small.png",
             width=100)

    st.markdown('<h1 class="title">Course Scheduler</h1>', unsafe_allow_html=True)

    course_code = st.text_input('Enter the desired course code:', value='', max_chars=10, key='course_code',
                                help='Enter course code here', )
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button('Generate Schedule'):
        run_app(course_code)


if __name__ == '__main__':
    main()
