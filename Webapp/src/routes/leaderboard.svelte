<script>
 let scores = [
    { name: "Alice", score: 120 },
    { name: "Bob", score: 95 },
    { name: "Charlie", score: 80 },
    { name: "Dana", score: 60 }
  ];
</script>

<div class="absolute inset-0 flex items-center justify-center">
    <div class="w-full max-w-md">
      <h1 class="text-2xl font-bold text-center">Leaderboard</h1>
      <ul class="divide-y divide-[#859a85]">
      {#each scores as { name, score }, i}
        <li class="flex justify-between py-3 px-2">
          <span>{i + 1}. {name}</span>
          <span class="font-semibold">{score}</span>
        </li>
      {/each}
      </ul>
    </div>
</div>
