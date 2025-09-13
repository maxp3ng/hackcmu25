<script>
  import Ip from './ip.svelte';
  import Leaderboard from './leaderboard.svelte';
  let page = $state("result"); //lb, result, running

  async function changePage(){
    if (page === "lb") {
      page = "result";
    }
    else if (page === "result") {
      page = "lb";
    }
    //console.log(page);
  }
</script>

<!-- general bg centering wrapper -->
<div class="min-h-screen bg-black text-white relative">

  <Ip/>
  <h1 class="absolute flex top-10 bottom-0 left-0 right-0 justify-center"> EcoDrive </h1>

  {#if page==="lb"}
    <Leaderboard/>
  {/if}

  <button class="absolute flex bottom-10 left-0 right-0 justify-center" onclick={changePage}> {page === "lb" ? "Start!" : (page === "result" ? "Reset..." : "" )}</button>
</div>


