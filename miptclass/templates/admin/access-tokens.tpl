<div class="container">
  <h1>Access Tokens</h1>

  {% if tokens %}
  <table class="table table-striped">
    <tr>
      <th>#</th><th>User Id</th><th>Access Token</th><th>Expires In</th>
    </tr>
    {% for token in tokens %}
    <tr>
      <td>{{ loop.index }}</td>
      <td><a href="https://vk.com/id{{ token[0] }}">{{ token[0] }}</td>
      {% for value in token[1:] %}
      <td>{{ value }}</td>
      {% endfor %}
    </tr>
    {% endfor %}
  </table>
  {% else %}
  <p>No valid tokens.</p>
  {% endif %}
</div>