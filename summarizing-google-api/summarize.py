import google.generativeai as palm
import asyncio
from pyppeteer import launch

import config


async def scrape_reviews(url):
    reviews = []

    browser = await launch({"headless": True, "args": ["--window-size=800,3200"]})

    page = await browser.newPage()
    await page.setViewport({"width": 800, "height": 3200})
    await page.goto(url)
    await page.waitForSelector(".jftiEf")

    elements = await page.querySelectorAll(".jftiEf")
    for element in elements:
        try:
            await page.waitForSelector(".w8nwRe")
            more_btn = await element.querySelector(".w8nwRe")
            await page.evaluate("button => button.click()", more_btn)
            await page.waitFor(5000)
        except:
            pass

        await page.waitForSelector(".MyEned")
        snippet = await element.querySelector(".MyEned")
        text = await page.evaluate("selected => selected.textContent", snippet)
        reviews.append(text)

    await browser.close()

    return reviews


def summarize(reviews, model):
    prompt = "I collected some reviews of a place I was considering visiting. \
        Can you summarize the reviews for me? I want to generally know what people \
        like and dislike. The reviews are below:\n"
    for review in reviews:
        prompt += "\n" + review

    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0,
        # The maximum length of the response
        max_output_tokens=300,
    )

    return completion.result


palm.configure(api_key=config.API_KEY)
models = [
    m for m in palm.list_models() if "generateText" in m.supported_generation_methods
]
model = models[0].name

url = input("Enter a url: ")

reviews = asyncio.get_event_loop().run_until_complete(scrape_reviews(url))

result = summarize(reviews, model)
print(result)
