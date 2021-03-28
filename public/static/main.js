var csrf = document.getElementById('csrf').value



function refreshPage() {
    setTimeout(() => {
        window.location.reload()
    }, 2000);
}

function login() {

    var username = document.getElementById('username').value

    if (username == '') {
        tata.error('Error', 'Username is required')
    }

    fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf,
            },
            body: JSON.stringify({
                'username': username
            })
        }).then(result => result.json())
        .then(response => {
            if (response.status_code == 200) {
                tata.success('Success', response.status_message)
               refreshPage()
            } else {
                // tata.error('Error', response.message)

            }

        })

}



function getRaffelTicket() {

    fetch('/api/get-ticket/')
        .then(result => result.json())
        .then(response => {
            console.log(response)
            if (response.status_code == 200) {
                tata.success('Success', response.status_message)
                refreshPage()
            } else {
                tata.error('Error', response.status_message)
            }

        })
}


function participate(id) {
    var element = document.getElementById(`participate_btn-${id}`)

    var lucky_draw_id = element.dataset.lucky_draw_id
    var ticket_id = element.dataset.ticket_id

    console.log(lucky_draw_id)
    console.log(ticket_id)

    fetch('/api/participate-in-game/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf,
            },
            body: JSON.stringify({
                'lucky_draw_id': lucky_draw_id,
                'ticket_id': ticket_id
            })
        }).then(result => result.json())
        .then(response => {
            if (response.status_code == 200) {
                tata.success('Success', response.status_message)
                refreshPage()
            } else {
                tata.error('Error', response.status_message)
            }
        })
}

