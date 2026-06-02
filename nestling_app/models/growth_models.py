import numpy as np
from scipy.optimize import curve_fit


# 📌 Growth Models
def logistic(x, a, k, x0):
    return a / (1 + np.exp(-k * (x - x0)))


def gompertz(x, a, b, c):
    return a * np.exp(-b * np.exp(-c * x))


def richards(x, a, k, x0, v):
    return a / (1 + np.exp(-k * (x - x0))) ** (1 / v)


def von_bertalanffy(x, l_inf, k, t0):
    return l_inf * (1 - np.exp(-k * (x - t0)))


def evf(x, a, b, c, d):
    return a * np.exp(-b * np.exp(-c * x)) * (1 - np.exp(-d * x))


# 📌 Information criteria calculation
INFORMATION_CRITERIA = {
    "AIC": "AIC",
    "AICC": "AICc",
}


def normalize_information_criterion(criterion):
    if not isinstance(criterion, str):
        raise ValueError("Unknown information criterion. Expected one of: AIC, AICc.")

    normalized = INFORMATION_CRITERIA.get(criterion.upper())
    if normalized is None:
        raise ValueError(f"Unknown information criterion '{criterion}'. Expected one of: AIC, AICc.")

    return normalized


def calculate_information_criteria(y_true, y_pred, params):
    n = len(y_true)
    residuals = y_true - y_pred
    sse = np.sum(residuals ** 2)
    k = len(params)

    aic = n * np.log(sse / n) + 2 * k
    aicc = np.inf
    if n > k + 1:
        aicc = aic + (2 * k * (k + 1)) / (n - k - 1)
    bic = n * np.log(sse / n) + k * np.log(n)

    return aic, aicc, bic


def calculate_aic_bic(y_true, y_pred, params):
    aic, _, bic = calculate_information_criteria(y_true, y_pred, params)
    return aic, bic


# 📌 Fit Models and Evaluate
def fit_models(x_data, y_data, criterion="AIC"):
    criterion = normalize_information_criterion(criterion)
    score_index = {
        "AIC": 2,
        "AICc": 3,
    }[criterion]
    delta_label = f"Δ{criterion}"

    models = {
        "Logistic": (logistic, [max(y_data), 1, np.median(x_data)]),
        "Gompertz": (gompertz, [max(y_data), 1, 0.1]),
        "Richards": (richards, [max(y_data), 1, np.median(x_data), 1]),
        "Von Bertalanffy": (von_bertalanffy, [max(y_data), 0.1, min(x_data)]),
        "Extreme Value Function": (evf, [max(y_data), 1, 0.1, 0.1])
    }

    results = []
    print("📦 Starting model fitting...")

    for model_name, (model_func, initial_params) in models.items():
        try:
            print(f"🔍 Trying model: {model_name}")
            popt, _ = curve_fit(model_func, x_data, y_data, p0=initial_params, maxfev=10000)
            y_pred = model_func(x_data, *popt)
            aic, aicc, bic = calculate_information_criteria(y_data, y_pred, popt)

            # Growth rate and inflection point
            if model_name == "Logistic":
                k_value, T_value = popt[1], popt[2]
            elif model_name == "Gompertz":
                k_value, T_value = popt[2], np.log(popt[1]) / popt[2]
            elif model_name == "Richards":
                k_value, T_value = popt[1], popt[2]
            elif model_name == "Von Bertalanffy":
                k_value, T_value = popt[1], popt[2]
            elif model_name == "Extreme Value Function":
                k_value, T_value = popt[2], np.log(popt[1]) / popt[2]
            else:
                k_value, T_value = None, None

            results.append((model_name, popt, aic, aicc, bic, k_value, T_value))
            print(f"✅ Success: {model_name} — {criterion}: {results[-1][score_index]:.2f}, k: {k_value:.4f}, T: {T_value:.2f}")

        except Exception as e:
            print(f"❌ Error with {model_name}: {e}")

    if not results:
        print("🚫 No models could be fitted.")
        return None, None

    results.sort(key=lambda x: x[score_index])
    best_score = results[0][score_index]
    scored_results = []
    for m, p, aic, aicc, bic, k, T in results:
        selected_score = {
            "AIC": aic,
            "AICc": aicc,
        }[criterion]
        delta = selected_score - best_score if np.isfinite(best_score) else np.inf
        scored_results.append((m, p, aic, aicc, bic, k, T, delta))
    results = scored_results

    best_delta = 0.0 if np.isfinite(best_score) else np.inf
    print(f"🏆 Best model: {results[0][0]} with {delta_label} = {best_delta:.1f}")
    return results[0], results
