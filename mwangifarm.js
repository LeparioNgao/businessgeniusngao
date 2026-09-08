// List the 40 cows that belong to Mwangi Farm.
const cowNames = [
  "Daisy", "Bella", "Kamau", "Zuri", "Nala", "Malaika", "Amani", "Imani",
  "Wanjiku", "Shiru", "Neema", "Pendo", "Baraka", "Jabali", "Kito", "Taji",
  "Asha", "Mumbi", "Nyambura", "Wairimu", "Chebet", "Njeri", "Wambui", "Atieno",
  "Akinyi", "Adhiambo", "Makena", "Mwende", "Wanjiru", "Muthoni", "Zawadi", "Tumaini",
  "Lulu", "Mrembo", "Kendi", "Sifa", "Furaha", "Jasiri", "Bahati", "Rehema"
];

// Create two simulated weekly milk records for every cow.
const milkRecords = cowNames.flatMap((cow, index) => {
  const weekOneLitres = 78 + index * 1.35;
  const weekTwoLitres = weekOneLitres + 5 + (index % 4) * 0.8;

  return [
    { cow, week: 1, litres: weekOneLitres, feed_kg: 42 + (index % 8) },
    { cow, week: 2, litres: weekTwoLitres, feed_kg: 45 + (index % 8) }
  ];
});

// Simulate an API response so the browser can practice the fetch pattern
// without connecting to a real dairy farm server.
const fakeFetch = () => Promise.resolve({
  ok: true,
  status: 200,
  json: () => Promise.resolve(milkRecords)
});

// Find the HTML elements that will display the records and receive clicks.
const display = document.querySelector("#farmDisplay");
const loadButton = document.querySelector("#loadFarmData");

// Fetch the milk records, calculate totals, and render week-two data in a table.
const loadMilkRecords = async () => {
  display.textContent = "Loading milk records...";

  try {
    const response = await fakeFetch();
    if (!response.ok) throw new Error(`Server error: ${response.status}`);

    // Parse the response, select week two, and calculate the farm summary.
    const records = await response.json();
    const weekTwoRecords = records.filter(record => record.week === 2);
    const totalLitres = weekTwoRecords.reduce((sum, record) => sum + record.litres, 0);
    const averagePerCow = totalLitres / weekTwoRecords.length;

    // Turn each selected record into one HTML table row.
    const rows = weekTwoRecords.map(record => `
      <tr>
        <td>${record.cow}</td>
        <td>${record.week}</td>
        <td>${record.litres.toFixed(1)} L</td>
        <td>${record.feed_kg} kg</td>
      </tr>
    `).join("");

    // Insert the summary cards and table into the page.
    display.innerHTML = `
      <div class="summary">
        <div><strong>${weekTwoRecords.length}</strong><span>Cows</span></div>
        <div><strong>${totalLitres.toFixed(1)} L</strong><span>Total milk</span></div>
        <div><strong>${averagePerCow.toFixed(1)} L</strong><span>Average per cow</span></div>
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Cow</th>
              <th>Week</th>
              <th>Milk yield</th>
              <th>Feed</th>
            </tr>
          </thead>
          <tbody>${rows}</tbody>
        </table>
      </div>
    `;

    console.log(`Records fetched: ${records.length}`);
    console.log(`Week 2 cows displayed: ${weekTwoRecords.length}`);
    console.log(`Total litres for week 2: ${totalLitres.toFixed(1)}`);
    console.log(`Average per cow: ${averagePerCow.toFixed(1)} L`);
  } catch (error) {
    // Show a readable message if the simulated request fails.
    display.textContent = `Fetch failed: ${error.message}`;
    console.error("Fetch failed:", error.message);
  }
};

// Load records when the button is clicked, and show the first result immediately.
loadButton.addEventListener("click", loadMilkRecords);
loadMilkRecords();
