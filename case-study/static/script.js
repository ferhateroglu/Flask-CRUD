// toggle modal

let topic = document.getElementById('topic')
let date = document.getElementById('date')
let start_time = document.getElementById('start_time')
let end_time = document.getElementById('end_time')
let participant_input = document.getElementById('participant-input')
let participant_list = document.getElementById('participant-list')

// toggle edit modal
let editTopic = document.getElementById('editTopic')
let editDate = document.getElementById('editDate')
let editStart_time = document.getElementById('editStart_time')
let editEnd_time = document.getElementById('editEnd_time')
let editParticipant_input = document.getElementById('editParticipant-input')
let editParticipant_list = document.getElementById('editParticipant-list')

let selectedMeetingId = null;


function toggleModal() {
    document.getElementById('modal').classList.toggle('hidden');
    // reset input fields
    topic.value = ''
    date.value = ''
    start_time.value = ''
    end_time.value = ''
    participant_input.value = ''
    participant_list.innerHTML = ''
}


// edit model
function toggleEditModal(event) {
    event.preventDefault();
    let targetElement;
    console.log(event.target.tagName)

    let currentState = document.getElementById('editModal').classList.toggle('hidden');
    // fill input fields
    if (!currentState) {

        if (event.target.tagName === 'svg') {
            targetElement = event.target.parentElement.parentElement.parentElement.parentElement;
            selectedMeetingId = event.target.dataset.id;
        } else {
            targetElement = event.target.parentElement.parentElement.parentElement.parentElement.parentElement;
            selectedMeetingId = event.target.parentElement.dataset.id;
        }

        console.log(targetElement);
        console.log(selectedMeetingId);
        let spanElements = targetElement.getElementsByTagName('span');

        editTopic.value = spanElements[0].innerText
        let participantArray = spanElements[1].innerText.split(', ');
        participantArray.forEach(participant => {
            const participantDiv = parentCreator(participant);
            editParticipant_list.appendChild(participantDiv);
        });
        console.log(participantArray);

        editDate.value = spanElements[2].innerText
        editStart_time.value = spanElements[3].innerText
        editEnd_time.value = spanElements[4].innerText

    } else {
        // reset input fields
        editTopic.value = ''
        editDate.value = ''
        editStart_time.value = ''
        editEnd_time.value = ''
        editParticipant_input.value = ''
        editParticipant_list.innerHTML = ''
        selectedMeetingId = null;
    }
}

participant_input.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault();

        const participantName = participant_input.value.trim();
        if (participantName !== '') {

            const participantDiv = parentCreator(participantName);

            const participantList = document.getElementById('participant-list');
            participantList.appendChild(participantDiv);

            participant_input.value = '';
        }
    }
});

editParticipant_input.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault();

        const participantName = editParticipant_input.value.trim();
        if (participantName !== '') {
            const participantDiv = parentCreator(participantName);
            editParticipant_list.appendChild(participantDiv);
            editParticipant_input.value = '';
        }
    }
});

function parentCreator(participantName) {
    const participantDiv = document.createElement('div');
    participantDiv.classList.add('bg-gray-200', 'rounded-full', 'px-4', 'py-2', 'hover:bg-red-300', 'cursor-pointer');
    participantDiv.innerHTML = participantName;
    participantDiv.onclick = function () {
        this.remove();
    }
    return participantDiv;
}

// submit meeting
function submitMeeting() {
    let participants = [];
    let participantDivs = participant_list.getElementsByTagName('div');
    for (let i = 0; i < participantDivs.length; i++) {
        participants.push(participantDivs[i].innerText);
    }
    let data = {
        topic: topic.value,
        date: date.value,
        start_time: start_time.value,
        end_time: end_time.value,
        participants: participants
    }
    // submit using fetch
    fetch('http://localhost:5000/meetings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => {
            if(response.status == 200){
                location.reload();
            }else if(response.status == 403){
                return response.json();
            }else{
                alert("Something went wrong");
            }
        })
        .then(data => {
            if(data){
                let keys = Object.keys(data);
                let errorString = "";
                let firstKey = keys[0];
                let errorArr = data[firstKey]
                errorString += firstKey + " " +errorArr[0];

                alert(errorString);
            }
         })
}

// update meeting
function updateMeeting() {

    let participants = [];
    let participantDivs = editParticipant_list.getElementsByTagName('div');
    for (let i = 0; i < participantDivs.length; i++) {
        participants.push(participantDivs[i].innerText);
    }
    let data = {
        topic: editTopic.value,
        date: editDate.value,
        start_time: editStart_time.value,
        end_time: editEnd_time.value,
        participants: participants
    }

    // submit using fetch
    fetch('http://localhost:5000/meetings/' + selectedMeetingId, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })	.then(response => {
            if(response.status == 200){
                location.reload();
            }else if(response.status == 403){
                return response.json();
            }else{
                alert("Something went wrong");
            }
        })
        .then(data => {
            if(data){
                let keys = Object.keys(data);
                let errorString = "";
                let firstKey = keys[0];
                let errorArr = data[firstKey]
                errorString += firstKey + " " +errorArr[0];

                alert(errorString);
            }
         })
}

// delete meeting
function deleteMeeting(event) {
    event.preventDefault();
    let meetingId = null;

    if (event.target.tagName === 'svg') {
        meetingId = event.target.dataset.id;
    } else {
        meetingId = event.target.parentElement.dataset.id;
    }

    fetch('http://localhost:5000/meetings/' + meetingId, {
        method: 'DELETE',
    })
        .then(response => response.json())
        .then(data => {
            location.reload();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}