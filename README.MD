## The problem/opportunity you identified

When starting this task, I struggled to think about how I could improve upon a stable and robust API—it is really simple. You send a POST request to an endpoint with the description of the presentation you want to generate and some extra parameters. On top of that, I don't have access to the functionality behind the endpoint, which means I couldn't change the output. I was limited to the creativity of my prompts.

This led me to think about how I could make it easier for the user to use the simple application. One way I initially thought of was adding narration to the resulting PowerPoint, making it a type of audiobook. However, there is already an extension on the website that converts the PowerPoint to a video with AI-generated narration.

That led me to use one of my favourite topics in AI, and in computing as a whole: Computer Vision! One thing that is missing from SlideSpeak's suite of tools is other means of generating presentations that are not through text. I could have taken the text approach and made it so that an application can utilize OCR to get text from an image and use that as a prompt. However, I took it one step further to give my approach some real-world value and a cool use case. I used a computer vision model that gives context of an image and used that as a prompt for the SlideSpeak API.

## Your approach to solving it

My approach to solving this was to find a model that can give context about an image. The next step was figuring out how I could serve this to the user. The easiest and most common way for this sort of task is through a website.

This meant that I would have to pick web technologies to make such a product. I opted to go with FastAPI for the backend as the CV model will be in Python. Therefore, keeping the language the same between the different stacks of the project will help speed up development and make testing easier.

For the frontend, I used Next.js. One personal reason was that I have never used Next.js or Tailwind CSS and I wanted to try them. In addition, I am comfortable with React, so it was a no-brainer to use something I can develop rapidly with, given the time constraint I had for the project. I only gave myself two days to do the project, so speed was the priority in this case with the designing, selecting the tools, and also the decisions around development.

Since the project has to be uploaded to GitHub for the interviewers, I am using GitHub as my version control. This meant that I could also utilize GitHub for my CI/CD flow. I used GitHub Actions to run my tests and build the FastAPI backend. Again, the choice to use this over something like Jenkins was the speed of development and the need to eliminate the parts where I would have to learn a new tool from scratch. I used Docker for containerization.

To deploy my project, if I am to get to that stage, I will use AWS because I haven't used AWS before and it provides simple computing and deployment processes for an application of my size and complexity. GCP was another alternative that I considered with Cloud Run or a VM, which I have professional experience with, but for the project I wanted to show I can learn on the fly and use another cloud provider to demonstrate my understanding of deployment methods. On AWS, the two options which I singled out for deployment were Lambda and EC2. I chose the latter for this project as there are two applications that will need to be deployed: the Next.js app and the FastAPI API. Lambda would require me to build the API with that in mind, which would constrain my creativity and limit the iterative approach I am aiming for in the project. Whereas an EC2 instance offers scalability and the ability to run the applications like I do locally.

## The value your solution provides to users

This provides lots of value to users by offering them another alternative to using text to generate a presentation. This also speeds up the process of generating a presentation by eliminating a barrier between the user and the output, which is typing. Moreover, the user can be more creative in terms of the presentation they want to make, as they are not limited by their proficiency in language and have a non-verbal way of communicating their ideas.