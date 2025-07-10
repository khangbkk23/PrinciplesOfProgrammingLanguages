# Lưu ý:
*Đọc AST*: Đọc đầu tiên từ lớp `Program`. Dễ nhất là liên tưởng đến ngôn ngữ quen  thuộc để dễ dịch từ kết quả ASTGEN.

*Đọc Exception*:
* RedeclaredDeclaration: khai báo lại. Catch lỗi và hiện thực.

`o: object`: Kiểu dữ liệu object => truyền mỗi bài khác nhau. Dùng để lưu trữ lịch sử phía trước đã được gọi. (thiết kế bằng stack, graph, tree, list, queue,...). Mở đầu là list rỗng và append vào mỗi lần gọi.