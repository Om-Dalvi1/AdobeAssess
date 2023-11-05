let sections = document.querySelectorAll('section');
let navLinks = document.querySelectorAll('header nav a');
window.onscroll = () => {
    sections.forEach(sec => {
        let top = window.scrollY;
        let offset = sec.offsetTop - 150;
        let height = sec.offsetHeight;
        let id = sec.getAttribute('id');
        if(top >= offset && top < offset + height) {
            navLinks.forEach(links => {
                links.classList.remove('active');
                document.querySelector('header nav a[href*=' + id + ']').classList.add('active');
            });
        };
    });
};

const information = [];


    // Define the functions to perform calculations

function calcLTV(appraisal, downPayment) {
    let loanAmount = appraisal - downPayment;
    return (loanAmount / appraisal) * 100;
}

function calcDTI(grossIncome, creditCardPMT, carPMT, studentPMT, mortgagePMT) {
    let totalPMT = creditCardPMT + carPMT + studentPMT + mortgagePMT;
    return (totalPMT / grossIncome) * 100;
}

function calcFEDTI(grossIncome, mortgagePMT) {
    return (mortgagePMT / grossIncome) * 100;
}

function validCreditScore(creditScore) {
    return creditScore >= 640;
}

function calcPMI(LTV, appraisal) {
    let PMI = 0;
    if (80 <= LTV && LTV < 95) {
        PMI = appraisal * 0.01 / 12;
    }
    return PMI;
}

function validLTV(LTV) {
    return LTV < 95;
}

function validDTI(DTI, FEDTI) {
    return DTI < 44 && FEDTI < 29;
}

// This is the main function that gets called when the user submits the form
function canBuyHouse(grossIncome, creditCardPMT, carPMT, studentPMT, appraisal, mortgagePMT, loanAMT, mortgagePMT, creditScore) {
   

    let LTV = calcLTV(appraisal, downPMT);
    let DTI = calcDTI(grossIncome, creditCardPMT, carPMT, studentPMT, mortgagePMT);
    let FEDTI = calcFEDTI(grossIncome, mortgagePMT);
    let PMI = calcPMI(LTV, appraisal);

    let isLTV = validLTV(LTV);
    let isDTI = validDTI(DTI, FEDTI);
    let isCredit = validCreditScore(creditScore);

    let approvalStatus = "Yes";

    let reasons = [];

    if (!isCredit) {
        approvalStatus = "No";
        reasons.push("Credit Score");
        return false;

    }
    if (!isLTV) {
        approvalStatus = "No";
        reasons.push("LTV");
        return false;

    }
    if (!isDTI) {
        if (DTI >= 44) reasons.push("DTI");
        if (FEDTI >= 29) reasons.push("FEDTI");
        return false;
    }
    return true;

    // This is where you would update the DOM with the result
    // For example, displaying the reasons why the user cannot buy a house

    // To prevent the form from submitting and refreshing the page
}
document.querySelector('.button').addEventListener('click',function(){

    // You would get these values from your HTML form inputs
    let grossIncome = parseFloat(document.getElementById('gMI').value);
    let creditCardPMT = parseFloat(document.getElementById('cred-card').value);
    let carPMT = parseFloat(document.getElementById('car').value);
    let studentPMT = parseFloat(document.getElementById('sdt-loans').value);
    let appraisal = parseFloat(document.getElementById('appraised').value);
    let downPMT = parseFloat(document.getElementById('down-pay').value);
    let loanAMT = parseFloat(document.getElementById('loans-amt').value);
    let mortgagePMT = parseFloat(document.getElementById('mortgage').value);
    let creditScore = parseInt(document.getElementById('cred-score').value);  

    assess = canBuyHouse(grossIncome, creditCardPMT, carPMT, studentPMT, appraisal, mortgagePMT, loanAMT, mortgagePMT, creditScore);
    if (assess === false){
        document.querySelector('.elegibility').textContent = 'Sorry, you are not eligeble to buy a home.';
    }
    else{
        document.querySelector('.eligebility').textContent = 'Congradulations, you are eligeble to buy a home.';
    }
    
})



function checkReason(reasons){
    const issue = '';
    // use some sort of iteration of the lists 
    return issue;
}

const issue = checkReason(dataRecieved);

issue = 'reason1';
if (issue === 'reason1'){
    document.querySelector('.issue1').textContent = 'Sorry, you are not eligeble to buy a home. Due to your Gross Monthly Income. Here are some suggestions:';
}
else{
    document.querySelector('.issue1').textContent = 'This is not an area of concern.';
}
if(issue === 'reason2'){
    document.querySelector('.issue2').textContent = 'Sorry, you are not eligeble to buy a home. Due to your Credit Card Payments. Here are some suggestions:';
}
else{
    document.querySelector('.issue2').textContent = 'This is not an area of concern.';
}
if(issue === 'reason3'){
    document.querySelector('.issue3').textContent = 'Sorry, you are not eligeble to buy a home. Due to your Credit Card Payments. Here are some suggestions:';
}
else{
    document.querySelector('.issue3').textContent = 'This is not an area of concern.';
}
if(issue === 'reason4'){
    document.querySelector('.issue4').textContent = 'Sorry, you are not eligeble to buy a home. Due to your Credit Card Payments. Here are some suggestions:';
}
else{
    document.querySelector('.issue4').textContent = 'This is not an area of concern.';
}
if(issue === 'reason5'){
    document.querySelector('.issue5').textContent = 'Sorry, you are not eligeble to buy a home. Due to your Credit Card Payments. Here are some suggestions:';
}
else{
    document.querySelector('.issue5').textContent = 'This is not an area of concern.';
}
if(issue === 'reason6'){
    document.querySelector('.issue6').textContent = 'Sorry, you are not eligeble to buy a home. Due to your Credit Card Payments. Here are some suggestions:';
}
else{
    document.querySelector('.issue6').textContent = 'This is not an area of concern.';
}
if(issue === 'reason7'){
    document.querySelector('.issue7').textContent = 'Sorry, you are not eligeble to buy a home. Due to your Credit Card Payments. Here are some suggestions:';
}
else{
    document.querySelector('.issue7').textContent = 'This is not an area of concern.';
}
if(issue === 'reason8'){
    document.querySelector('.issue8').textContent = 'Sorry, you are not eligeble to buy a home. Due to your Credit Card Payments. Here are some suggestions:';
}
else{
    document.querySelector('.issue8').textContent = 'This is not an area of concern.';
}

if(issue === 'reason9'){
    document.querySelector('.issue9').textContent = 'Sorry, you are not eligeble to buy a home. Due to your Credit Card Payments. Here are some suggestions:';
}
else{
    document.querySelector('.issue9').textContent = 'This is not an area of concern.';
}

