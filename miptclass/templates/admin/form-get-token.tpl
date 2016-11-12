<div class="container">
  <h1>Getting Tokens</h1>

  <form class="form-inline" action="{% autoescape false %}{{ action }}{% endautoescape %}" method="POST">
    <div class="form-group">
      <label for="submit">Login in VKontakte:</label>
      <input class="btn btn-default" name="submit" type="submit" value="Login">
    </div>
  </form>
</div>