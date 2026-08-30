import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    import numpy as np

    return (np,)


@app.cell
def _(np):
    class SimpleLinearRegression:
        def __init__(self):
            self.coefficient_ = None
            self.intercept_ = None
            self.r2score_ = None

        def fit(self, X, y):
            n = len(X)
            X_b = np.concatenate((np.ones((n, 1)), X), axis=1)
            self.coefficient_ = np.linalg.inv(X_b.T.dot(X_b))
            self.intercept_ = self.coefficient_[0]
            y_pred = X_b.dot(self.coefficient_)
            self.r2score_ = 1 - (np.sum((y-y_pred)**2)) / np.sum((y - np.mean(y))**2)

    return


if __name__ == "__main__":
    app.run()
