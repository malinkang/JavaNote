# 网络编程

```java
// https://api.weibo.com/2/trends/hourly.json
HttpURLConnection connection = (HttpURLConnection) new URL("https://api.weibo.com/2/trends/hourly.json").openConnection();
connection.setConnectTimeout(30 * 1000);//
connection.setReadTimeout(20 * 1000);
connection.setRequestMethod("GET");
connection.setDoInput(true);
connection.setDoOutput(true);
ByteArrayOutputStream content = new ByteArrayOutputStream();
// 多个参数使用&
content.write("source".getBytes("UTF-8"));
content.write('=');
content.write("2996785772".getBytes("UTF-8"));
connection.getOutputStream().write(content.toByteArray());
int status = connection.getResponseCode();
String reason = connection.getResponseMessage();
BufferedReader in = new BufferedReader(
        new InputStreamReader(connection.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();

while ((inputLine = in.readLine()) != null) {
        response.append(inputLine);
}
System.out.println(response);
in.close();
```

