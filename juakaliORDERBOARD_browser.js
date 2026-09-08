const orderForm = document.querySelector('#orderForm');
const clientNameInput = document.querySelector('#clientName');
const jobTypeInput = document.querySelector('#jobType');
const quoteKesInput = document.querySelector('#quoteKes');
const orderList = document.querySelector('#orderList');
const summary = document.querySelector('#summary');

const processOrder = (clientName, jobType, quoteKes) => {
  const isLargeJob = quoteKes >= 10000;
  const priority = isLargeJob ? 'High' : 'Normal';
  return `Client: ${clientName} | Job: ${jobType} | Quote: KES ${quoteKes.toLocaleString()} | Priority: ${priority}`;
};

let totalQuoted = 0;

orderForm.addEventListener('submit', (event) => {
  event.preventDefault();

  const clientName = clientNameInput.value.trim();
  const jobType = jobTypeInput.value.trim();
  const quoteKes = Number(quoteKesInput.value);

  if (!clientName || !jobType || Number.isNaN(quoteKes) || quoteKes <= 0) {
    alert('Please enter valid client name, job type, and quote.');
    return;
  }

  const orderText = processOrder(clientName, jobType, quoteKes);

  const li = document.createElement('li');
  li.textContent = orderText;
  orderList.appendChild(li);

  totalQuoted += quoteKes;
  summary.textContent = `Total quoted today: KES ${totalQuoted.toLocaleString()}`;

  orderForm.reset();
  clientNameInput.focus();
});
