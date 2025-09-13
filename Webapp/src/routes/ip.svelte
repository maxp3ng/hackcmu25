<script>
    let ip = $state("Click for ip");
    
    async function getIp() {
        const res = await fetch('/api/ip', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ })
        });
        const data = await res.json()
        let response = data.ip;
        return response;
    }

    async function ipClick(){
        console.log("clicked ip");
        ip = await(getIp());
    }
</script>

<button onclick={ipClick} class="absolute right-10 top-5 flex"> {ip} </button>
