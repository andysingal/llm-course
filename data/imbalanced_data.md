[Solving the Imbalanced Data Problem in RAG](https://www.c-sharpcorner.com/article/solving-the-imbalanced-data-problem-in-rag/)

To sample from an imbalanced dataset without external libraries like NumPy, we use the Cumulative Distribution Function (CDF) + Binary Search approach.

- Calculate cumulative weights by transforming the raw weights into a running total.

- Generate a random target between 0 and the total weight.

- Use Python's built-in bisect module to efficiently locate the selected index.
