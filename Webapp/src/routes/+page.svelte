<script>
  import Ip from './ip.svelte';
  import Leaderboard from './leaderboard.svelte';
  let page = $state("result"); //lb, result, running
  let imgVersion = Date.now();
  let imageUrl = '/plot.png';

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

  {#if page==="result"}
    <img src={`/plot.png?${imgVersion}`} alt="plot" width="600" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
  {/if}
  <!-- <button class="absolute flex bottom-10 left-0 right-0 justify-center" onclick={changePage}> {page === "lb" ? "Start!" : (page === "result" ? "Reset..." : "" )}</button> -->
</div>


