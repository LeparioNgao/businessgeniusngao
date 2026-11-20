const form = document.getElementById("marketForm");
const coinInput = document.getElementById("coinInput");
const currencyInput = document.getElementById("currencyInput");
const result = document.getElementById("result");

function formatMoney(amount, currency) {
  if (amount === null || amount === undefined) {
    return "Not available";
  }

  return `${currency} ${Number(amount).toLocaleString(undefined, {
    minimumFractionDigits: amount >= 1 ? 2 : 8,
    maximumFractionDigits: amount >= 1 ? 2 : 8,
  })}`;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const coin = coinInput.value.trim().toLowerCase();
  const currency = currencyInput.value.trim().toLowerCase() || "usd";

  if (!coin) {
    result.className = "result error";
    result.textContent = "Please enter a CoinGecko coin ID.";
    return;
  }

  result.className = "result";
  result.textContent = "Loading...";

  try {
    const response = await fetch(
      `/api/snapshot?coin=${encodeURIComponent(coin)}&currency=${encodeURIComponent(currency)}`
    );
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || `Request failed (${response.status})`);
    }

    const change = data.price_change_percentage_24h;
    const changeClass = change === null || change === undefined
      ? ""
      : change >= 0 ? "positive" : "negative";
    const changeText = change === null || change === undefined
      ? "Not available"
      : `${change >= 0 ? "+" : ""}${change.toFixed(2)}%`;

    result.innerHTML = `
      <section class="snapshot">
        <h2>${data.name} (${data.symbol})</h2>
        <div class="metric">
          <span>Current price</span>
          <strong>${formatMoney(data.current_price, data.currency)}</strong>
        </div>
        <div class="metric">
          <span>Market capitalization</span>
          <strong>${formatMoney(data.market_cap, data.currency)}</strong>
        </div>
        <div class="metric">
          <span>24-hour trading volume</span>
          <strong>${formatMoney(data.total_volume_24h, data.currency)}</strong>
        </div>
        <div class="metric">
          <span>24-hour price change</span>
          <strong class="${changeClass}">${changeText}</strong>
        </div>
      </section>
    `;
  } catch (error) {
    result.className = "result error";
    result.textContent = `Error: ${error.message}`;
  }
});
