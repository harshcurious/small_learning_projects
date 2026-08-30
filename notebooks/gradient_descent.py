import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium", auto_download=["ipynb"])


@app.cell
def _():
    import altair as alt
    import marimo as mo
    import numpy as np
    import pandas as pd

    return alt, mo, np, pd


@app.cell
def _(np):
    rng = np.random.default_rng(42)
    return (rng,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Gradient Descent for Linear Regression

    We generate data from

    $$y = 5x + 20 + \epsilon, \qquad \epsilon \sim \mathcal{N}(0, 3^2)$$

    Each epoch visits every datapoint in its fixed order. The parameters are updated after each datapoint, and the full-dataset mean squared error is recorded after the epoch.
    """)
    return


@app.cell(hide_code=True)
def _(mo, np):
    is_script_mode = mo.app_meta().mode == "script"

    def validate_controls(values):
        if values is None:
            return None

        integer_fields = {
            "n_custom": "Custom data size",
            "epochs_custom": "Custom epochs",
            "batch_size_custom": "Custom batch size",
        }
        for key, label in integer_fields.items():
            value = values[key]
            if value is not None and (
                not np.isfinite(value)
                or value <= 0
                or not float(value).is_integer()
            ):
                return f"{label} must be a positive integer."

        alpha = values["alpha_custom"]
        if alpha is not None and (not np.isfinite(alpha) or alpha <= 0):
            return "Custom learning rate must be positive."
        return None

    n_preset = mo.ui.dropdown(
        options=[100, 500, 1_000, 5_000],
        value=1_000,
        label="Preset",
    )
    n_custom = mo.ui.number(
        step=1,
        value=None,
        label="Custom N (optional)",
    )
    epochs_preset = mo.ui.dropdown(
        options=[10, 50, 100, 500, 1_000],
        value=100,
        label="Preset",
    )
    epochs_custom = mo.ui.number(
        step=1,
        value=None,
        label="Custom epochs (optional)",
    )
    alpha_preset = mo.ui.dropdown(
        options=[0.0001, 0.0005, 0.001, 0.005, 0.01],
        value=0.001,
        label="Preset",
    )
    alpha_custom = mo.ui.number(
        value=None,
        label="Custom alpha (optional)",
    )
    batch_size_preset = mo.ui.dropdown(
        options=[8, 16, 32, 64, 128],
        value=32,
        label="Preset",
    )
    batch_size_custom = mo.ui.number(
        step=1,
        value=None,
        label="Custom batch size (optional)",
    )
    gradient_aggregation = mo.ui.dropdown(
        options=["mean", "sum"],
        value="mean",
        label="Gradient aggregation",
    )

    run_form = (
        mo.md(r"""
        ## Experiment controls

        **Data size**  \
        {n_preset} {n_custom}

        **Epochs**  \
        {epochs_preset} {epochs_custom}

        **Learning rate ($\alpha$)**  \
        {alpha_preset} {alpha_custom}

        **Mini-batch size**  \
        {batch_size_preset} {batch_size_custom}

        **Mini-batch gradient aggregation**  \
        {gradient_aggregation}
        """)
        .batch(
            n_preset=n_preset,
            n_custom=n_custom,
            epochs_preset=epochs_preset,
            epochs_custom=epochs_custom,
            alpha_preset=alpha_preset,
            alpha_custom=alpha_custom,
            batch_size_preset=batch_size_preset,
            batch_size_custom=batch_size_custom,
            gradient_aggregation=gradient_aggregation,
        )
        .form(
            submit_button_label="Run",
            validate=validate_controls,
            clear_on_submit=False,
        )
    )

    run_form  # noqa: B018
    return (
        batch_size_custom,
        batch_size_preset,
        is_script_mode,
        n_custom,
        n_preset,
        run_form,
    )


@app.cell(hide_code=True)
def batchWarn(batch_size_custom, batch_size_preset, mo, n_custom, n_preset):
    selected_n = n_custom.value or n_preset.value
    selected_batch_size = batch_size_custom.value or batch_size_preset.value

    if selected_batch_size > selected_n:
        mo.callout(
            f"Batch size ({int(selected_batch_size)}) exceeds N ({int(selected_n)}); "
            "mini-batch GD will use one full batch.",
            kind="warn",
        )
    return


@app.cell(hide_code=True)
def _(is_script_mode, run_form):
    defaults = {
        "n": 1_000,
        "epochs": 100,
        "alpha": 0.001,
        "batch_size": 32,
        "aggregation": "mean",
    }
    submitted = None if is_script_mode else run_form.value

    if submitted is None:
        run_config = defaults
    else:
        run_config = {
            "n": int(submitted["n_custom"] or submitted["n_preset"]),
            "epochs": int(
                submitted["epochs_custom"] or submitted["epochs_preset"]
            ),
            "alpha": float(
                submitted["alpha_custom"] or submitted["alpha_preset"]
            ),
            "batch_size": int(
                submitted.get("batch_size_custom")
                or submitted.get("batch_size_preset", defaults["batch_size"])
            ),
            "aggregation": submitted.get(
                "gradient_aggregation", defaults["aggregation"]
            ),
        }
    return (run_config,)


@app.cell(hide_code=True)
def _(np, rng, run_config):
    X = np.linspace(5, 10, run_config["n"])
    Y = 5 * X + 20 + rng.normal(loc=0, scale=3, size=run_config["n"])
    return X, Y


@app.cell
def _(X, Y, np, run_config):
    def train_gd(
        X, Y, epochs, alpha, initial_slope=0.0, initial_intercept=0.0
    ):
        """
        Trains full-batch gradient descent on mean squared error.
        """
        slope = initial_slope
        intercept = initial_intercept
        losses = [float(np.mean((Y - (slope * X + intercept)) ** 2))]
        slope_history = [slope]
        intercept_history = [intercept]

        for _ in range(epochs):
            residual = Y - (slope * X + intercept)
            slope += 2 * alpha * np.mean(residual * X)
            intercept += 2 * alpha * np.mean(residual)

            predictions = slope * X + intercept
            losses.append(float(np.mean((Y - predictions) ** 2)))
            slope_history.append(slope)
            intercept_history.append(intercept)

        return {
            "losses": np.array(losses),
            "slope_history": np.array(slope_history),
            "intercept_history": np.array(intercept_history),
        }

    gd_results = train_gd(
        X,
        Y,
        epochs=run_config["epochs"],
        alpha=run_config["alpha"],
        initial_slope=4,
        initial_intercept=10,
    )
    return (gd_results,)


@app.cell
def _(alt, gd_results, pd):
    loss_data_gd = pd.DataFrame(
        {
            "epoch": range(len(gd_results["losses"])),
            "mse": gd_results["losses"],
            "slope": gd_results["slope_history"],
            "intercept": gd_results["intercept_history"],
        }
    )
    loss_chart_gd = (
        alt.Chart(loss_data_gd)
        .mark_line(point=True, color="#2563eb")
        .encode(
            x=alt.X(
                "epoch:Q",
                title="Epoch",
                axis=alt.Axis(grid=True, gridWidth=1.5, gridOpacity=0.6),
            ),
            y=alt.Y(
                "mse:Q",
                title="Mean squared error",
                scale=alt.Scale(type="log"),
                axis=alt.Axis(grid=True, gridWidth=1.5, gridOpacity=0.6),
            ),
            tooltip=[
                alt.Tooltip("epoch:Q", title="Epoch"),
                alt.Tooltip("mse:Q", title="MSE", format=".4f"),
                alt.Tooltip("slope:Q", title="Slope", format=".2f"),
                alt.Tooltip("intercept:Q", title="Intercept", format=".2f"),
            ],
        )
        .properties(
            title="Full-dataset MSE after each epoch",
            width="container",
            height=450,
        )
    )
    loss_chart_gd
    return


@app.cell
def _(gd_results, mo, run_config):
    gd_final_slope = gd_results["slope_history"][-1]
    gd_final_intercept = gd_results["intercept_history"][-1]
    gd_final_loss = gd_results["losses"][-1]

    mo.md(f"""
    ### Gradient Descent final parameters

    - Data points: `{run_config["n"]}`
    - Epochs: `{run_config["epochs"]}`
    - Learning rate: `{run_config["alpha"]:g}`
    - Slope: `{gd_final_slope:.4f}`
    - Intercept: `{gd_final_intercept:.4f}`
    - Final MSE: `{gd_final_loss:.4f}`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Stochastic Gradient Descent for Linear Regression
    """)
    return


@app.cell(hide_code=True)
def _(X, Y, np, run_config):
    def train_sgd(
        X, Y, epochs, alpha, initial_slope=0.0, initial_intercept=0.0
    ):
        slope = initial_slope
        intercept = initial_intercept
        losses = [float(np.mean((Y - (slope * X + intercept)) ** 2))]
        slope_history = [slope]
        intercept_history = [intercept]

        for _ in range(epochs):
            for x_i, y_i in zip(X, Y):
                residual = y_i - (slope * x_i + intercept)
                slope += 2 * alpha * residual * x_i
                intercept += 2 * alpha * residual

            predictions = slope * X + intercept
            losses.append(float(np.mean((Y - predictions) ** 2)))
            slope_history.append(slope)
            intercept_history.append(intercept)

        return {
            "losses": np.array(losses),
            "slope_history": np.array(slope_history),
            "intercept_history": np.array(intercept_history),
        }

    sgd_results = train_sgd(
        X,
        Y,
        epochs=run_config["epochs"],
        alpha=run_config["alpha"],
    )
    return (sgd_results,)


@app.cell(hide_code=True)
def _(alt, pd, sgd_results):
    sgd_loss_data = pd.DataFrame(
        {
            "epoch": range(len(sgd_results["losses"])),
            "mse": sgd_results["losses"],
            "slope": sgd_results["slope_history"],
            "intercept": sgd_results["intercept_history"],
        }
    )
    sgd_loss_chart = (
        alt.Chart(sgd_loss_data)
        .mark_line(point=True, color="#2563eb")
        .encode(
            x=alt.X(
                "epoch:Q",
                title="Epoch",
                axis=alt.Axis(grid=True, gridWidth=1.5, gridOpacity=0.6),
            ),
            y=alt.Y(
                "mse:Q",
                title="Mean squared error",
                scale=alt.Scale(type="log"),
                axis=alt.Axis(grid=True, gridWidth=1.5, gridOpacity=0.6),
            ),
            tooltip=[
                alt.Tooltip("epoch:Q", title="Epoch"),
                alt.Tooltip("mse:Q", title="MSE", format=".4f"),
                alt.Tooltip("slope:Q", title="Slope", format=".2f"),
                alt.Tooltip("intercept:Q", title="Intercept", format=".2f"),
            ],
        )
        .properties(
            title="Full-dataset MSE after each epoch",
            width="container",
            height=450,
        )
    )
    sgd_loss_chart
    return


@app.cell(hide_code=True)
def _(mo, run_config, sgd_results):
    sgd_final_slope = sgd_results["slope_history"][-1]
    sgd_final_intercept = sgd_results["intercept_history"][-1]
    sgd_final_loss = sgd_results["losses"][-1]

    mo.md(f"""
    ### Stochastic Gradiant Descent final parameters

    - Data points: `{run_config["n"]}`
    - Epochs: `{run_config["epochs"]}`
    - Learning rate: `{run_config["alpha"]:g}`
    - Slope: `{sgd_final_slope:.4f}`
    - Intercept: `{sgd_final_intercept:.4f}`
    - Final MSE: `{sgd_final_loss:.4f}`
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Mini-Batch Gradient Descent for Linear Regression

    Mini-batch gradient descent shuffles the data at the start of each epoch,
    then updates the parameters after each batch. The final batch is included even
    when it is smaller than the configured batch size.
    """)
    return


@app.cell(hide_code=True)
def train_minibatch_cell(X, Y, np, rng, run_config):
    def train_minibatch(
        X,
        Y,
        epochs,
        alpha,
        batch_size,
        rng,
        aggregation="mean",
        initial_slope=0.0,
        initial_intercept=0.0,
    ):
        if aggregation not in {"mean", "sum"}:
            raise ValueError("aggregation must be 'mean' or 'sum'")

        slope = initial_slope
        intercept = initial_intercept
        batch_size = min(batch_size, len(X))
        indices = np.arange(len(X))
        losses = [float(np.mean((Y - (slope * X + intercept)) ** 2))]
        slope_history = [slope]
        intercept_history = [intercept]

        for _ in range(epochs):
            rng.shuffle(indices)
            for start in range(0, len(X), batch_size):
                batch_indices = indices[start : start + batch_size]
                x_batch = X[batch_indices]
                y_batch = Y[batch_indices]
                residual = y_batch - (slope * x_batch + intercept)

                if aggregation == "mean":
                    slope_gradient = np.mean(residual * x_batch)
                    intercept_gradient = np.mean(residual)
                else:
                    slope_gradient = np.sum(residual * x_batch)
                    intercept_gradient = np.sum(residual)

                slope += 2 * alpha * slope_gradient
                intercept += 2 * alpha * intercept_gradient

            predictions = slope * X + intercept
            losses.append(float(np.mean((Y - predictions) ** 2)))
            slope_history.append(slope)
            intercept_history.append(intercept)

        return {
            "losses": np.array(losses),
            "slope_history": np.array(slope_history),
            "intercept_history": np.array(intercept_history),
        }

    minibatch_results = train_minibatch(
        X,
        Y,
        epochs=run_config["epochs"],
        alpha=run_config["alpha"],
        batch_size=run_config["batch_size"],
        rng=rng,
        aggregation=run_config["aggregation"],
    )
    return (minibatch_results,)


@app.cell(hide_code=True)
def minibatch_chart(alt, minibatch_results, pd):
    minibatch_loss_data = pd.DataFrame(
        {
            "epoch": range(len(minibatch_results["losses"])),
            "mse": minibatch_results["losses"],
            "slope": minibatch_results["slope_history"],
            "intercept": minibatch_results["intercept_history"],
        }
    )
    minibatch_loss_chart = (
        alt.Chart(minibatch_loss_data)
        .mark_line(point=True, color="#2563eb")
        .encode(
            x=alt.X(
                "epoch:Q",
                title="Epoch",
                axis=alt.Axis(grid=True, gridWidth=1.5, gridOpacity=0.6),
            ),
            y=alt.Y(
                "mse:Q",
                title="Mean squared error",
                scale=alt.Scale(type="log"),
                axis=alt.Axis(grid=True, gridWidth=1.5, gridOpacity=0.6),
            ),
            tooltip=[
                alt.Tooltip("epoch:Q", title="Epoch"),
                alt.Tooltip("mse:Q", title="MSE", format=".4f"),
                alt.Tooltip("slope:Q", title="Slope", format=".2f"),
                alt.Tooltip("intercept:Q", title="Intercept", format=".2f"),
            ],
        )
        .properties(
            title="Mini-batch full-dataset MSE after each epoch",
            width="container",
            height=450,
        )
    )
    minibatch_loss_chart
    return


@app.cell(hide_code=True)
def minibatch_summary(minibatch_results, mo, run_config):
    minibatch_final_slope = minibatch_results["slope_history"][-1]
    minibatch_final_intercept = minibatch_results["intercept_history"][-1]
    minibatch_final_loss = minibatch_results["losses"][-1]

    mo.md(f"""
    ### Mini-batch Gradient Descent final parameters

    - Data points: `{run_config["n"]}`
    - Epochs: `{run_config["epochs"]}`
    - Learning rate: `{run_config["alpha"]:g}`
    - Batch size: `{run_config["batch_size"]}`
    - Gradient aggregation: `{run_config["aggregation"]}`
    - Slope: `{minibatch_final_slope:.4f}`
    - Intercept: `{minibatch_final_intercept:.4f}`
    - Final MSE: `{minibatch_final_loss:.4f}`
    """)
    return


if __name__ == "__main__":
    app.run()
