import google.generativeai as palm
import asyncio
from pyppeteer import launch

import config

async def scrape_reviews(url):
    reviews = []
    browser = await launch({"headless": True, "args": [
            '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            '--user-data-dir=/tmp/user_data/',
            '--window-size=800,3200',
        ]})
    page = await browser.newPage()

    await page.setViewport({"width": 800, "height": 3200})
    await page.goto(url)

    await page.waitForSelector('.jftiEf')
    elements = await page.querySelectorAll('.jftiEf')
    for element in elements:
        # element.getElementBy
        await page.waitForSelector('.w8nwRe')
        more_btn = await element.querySelector('.w8nwRe')
        if more_btn:
            await page.evaluate('button => button.click()', more_btn)
            await page.waitFor(6000)

        snippet = await element.querySelector('.MyEned')
        text = await page.evaluate('(element) => element.textContent', snippet)
        
        reviews.append(text)
    await browser.close()

    return reviews

def summarize(reviews, model):
    prompt = "I collected some reviews about this place that I am considering visiting. Can you summarize the reviews for me? I want to know what people like and dislike about the place."
    for i in range(len(reviews)):
        prompt += f"\n{i+1}. {reviews[i]}"

    completion = palm.generate_text(
            model=model,
            prompt=prompt,
            # The variety of the responses
            # 0 is more predictable, 1 is more creative (higher risk of hallucinations)
            temperature=0,
            # The maximum length of the response
            max_output_tokens=500,
        )
    
    return completion.result

if __name__ == "__main__":
    palm.configure(api_key=config.API_KEY)
    models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
    model = models[0].name
    
    while True:
        user_input = input("Which reviews do you want to summarize? Paste a link or click 'q' to exit.\n")
        if user_input == "q": break
        try:
            reviews = asyncio.get_event_loop().run_until_complete(scrape_reviews(user_input))
            print(summarize(reviews, model))

        except:
            print("Sorry, that didn't quite work. Let's try again.")
            continue