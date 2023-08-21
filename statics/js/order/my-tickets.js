// *** Change all price to thousand separator text
function numberWithCommas(x) {
    return x.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
}
Array.from(document.querySelectorAll('.price-value')).forEach(elem => {
    elem.innerHTML = numberWithCommas(elem.innerHTML);
})




const tickets = document.querySelectorAll('.ticket');
const ticketsPopup = document.querySelectorAll('.ticket-popup-box');

// *** Show popup for every ticket after click on the 'detail-box'
Array.from(tickets).forEach(ticket => {
    ticket.addEventListener('click', e => {
        if(e.target.closest('.detail-box')){
            Array.from(ticketsPopup).forEach(ticketPopup => {
                if(ticketPopup.getAttribute('data-ticketsold-id') == ticket.getAttribute('data-ticketsold-id')){
                    ticketPopup.classList.remove('d-none');
                }
            })
        }
    })
})



// *** Close popup by 'click on the close button' and 'click on the outside of the popup'
Array.from(ticketsPopup).forEach(ticketPopup => {
    ticketPopup.addEventListener('click', e => {
        if(!ticketPopup.classList.contains('d-none')){
            // Click on the close button
            if(e.target.closest('.close-button')){
                ticketPopup.classList.add('d-none');
            }
            // click outside the popup-box
            if(!e.target.closest('.ticket-popup')){
                ticketPopup.classList.add('d-none');
            }
        }
    })
})

// *** Close popup by 'press escape' key
Array.from(ticketsPopup).forEach(ticketPopup => {
    document.addEventListener('keyup', e => {
        if(!ticketPopup.classList.contains('d-none')){
            if(e.key == 'Escape'){
                ticketPopup.classList.add('d-none');
            }
        }
    })
})





// *** copy ticket-number code to clipboard
// ? IMPORTANT: 'navigator.clipboard.writeText is a Promise object then this method must be invoked as a async method 
const copyContent = async (content, copyButton) => {
    try {
      await navigator.clipboard.writeText(content);
      let newElem = document.createElement('div');
      newElem.innerHTML = 'copied';
      newElem.style.width = 'max-content';
      newElem.style.padding = '3px';
      newElem.style.backgroundColor = 'black';
      newElem.style.color = 'white';
      newElem.style.position = 'absolute';
    //   newElem.style.top = '2px';
    //   newElem.style.left = '2px';
      newElem.style.borderRadius = '4px';
      copyButton.appendChild(newElem)
      setTimeout(() => {
        newElem.remove();
      }, 1500)
    } catch (err) {
      console.error('Failed to copy: ', err);
    }
}

Array.from(ticketsPopup).forEach(ticketPopup => {
    ticketPopup.addEventListener('click', e => {
        if(!ticketPopup.classList.contains('.d-none')){
            const copyButton = ticketPopup.querySelector('.fa-copy');
            const ticketNumberCode = ticketPopup.querySelector('.code').innerHTML;
            if(e.target == copyButton){
                copyContent(ticketNumberCode, copyButton);
            }
        }
    })
})