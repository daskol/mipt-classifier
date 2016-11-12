<div class="container">
  <h1>Brief Info</h1>

  <p>
  Total users: {{ stat['num_users'] }}
  Total friends: {{ stat['num_friends'] }}
  Total groups: {{ stat['num_groups'] }}
  Total tokens: {{ stat['num_tokens'] }}</p>

  <table class="table">
    <tr><th>#</th><th>Metic</th><th>Value</th></tr>
    <tr><td>1</td><td>Total users</td><td>{{ stat['num_users'] }}</td></tr>
    <tr><td>2</td><td>Total friends</td><td>{{ stat['num_friends'] }}</td></tr>
    <tr><td>3</td><td>Total groups</td><td>{{ stat['num_groups'] }}</td></tr>
    <tr><td>4</td><td>Total tokens</td><td>{{ stat['num_tokens'] }}</td></tr>
  </table>
</div>  