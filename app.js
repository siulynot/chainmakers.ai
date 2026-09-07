"use strict";
function workflowMailto(data){const subject=`Workflow inquiry from ${data.company}`;const body=`Name: ${data.name}\nCompany: ${data.company}\nEmail: ${data.email}\n\nProcess to fix:\n${data.process}\n\nHow it works today:\n${data.today}`;return `mailto:chainmakerspr@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`}
if(typeof module!=="undefined")module.exports={workflowMailto};
if(typeof document!=="undefined"){
 const form=document.querySelector("#workflow-form");
 document.querySelectorAll("[data-interest]").forEach(link=>link.addEventListener("click",()=>document.querySelector("#contact").scrollIntoView({behavior:"smooth"})));
 form.addEventListener("submit",event=>{event.preventDefault();if(!form.reportValidity())return;const data=Object.fromEntries(new FormData(form).entries());window.location.href=workflowMailto(data);document.querySelector("#form-status").textContent="Review the prepared email and send it when you're ready. If it did not open, email chainmakerspr@gmail.com."});
}
