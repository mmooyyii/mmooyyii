// 实现http流式下载. 可以用来实现下载大型类似于csv的流式文件,
// 可以在服务端没有完整文件的情况下,客户端就立即开始开始下载.
// 如果有办法知道文件的总大小, 可以在header加上 `w.Header().Add("Content-Length", "{文件总字节数}")`
// 这样可以在浏览器上看到进度
// 另一种做法是用Content-Range, 还可以支持断点续传, 不过如果一开始没有一个完整文件的话实现起来会比较复杂.

package main

import (
	"fmt"
	"io"
	"net/http"
	"strings"
	"time"
)

func main() {
	port := 12354
	http.HandleFunc("/download", handleDownload)
	addr := fmt.Sprintf(":%d", port)
	fmt.Println("Start ", addr)
	fmt.Println("下载文件: wget http://localhost:12354/download")
	err := http.ListenAndServe(addr, nil)
	if err != nil {
		fmt.Println(err.Error())
		return
	}
}

type SlowReader struct {
	a int
}

func (s *SlowReader) Read(p []byte) (n int, err error) {
	time.Sleep(time.Second / 10)
	if s.a == 0 {
		return 0, io.EOF
	}
	s.a -= 1
	n = copy(p, strings.Repeat("1", 1000))
	return
}

func handleDownload(w http.ResponseWriter, request *http.Request) {
	//打开文件
	file := &SlowReader{a: 100}
	//设置响应的header头
	w.Header().Add("Access-Control-Allow-Origin", "*")
	w.Header().Add("Content-type", "application/octet-stream")
	w.Header().Add("content-disposition", "attachment; filename=hello")
	//将文件写至responseBody
	_, err := io.Copy(w, file)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		_, _ = io.WriteString(w, "Bad request")
		return
	}
}
