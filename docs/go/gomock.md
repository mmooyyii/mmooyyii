下面2个函数的写法
```go
func GetNumberOfStudent1(age int) int {
	conn := db.NewMysql()
	if 0 < age && age < 18 {
		return conn.Query("select count(*) from students where age = 18")
	} else {
		return 0
	}
}
func GetNumberOfStudent2(conn db.DatabaseConnect, age int) int {
	if 0 < age && age < 18 {
		return conn.Query("select count(*) from students where age = 18")
	} else {
		return 0
	}
}
```
GetNumberOfStudent1的conn在函数中获得，GetNumberOfStudent2的从参数中传入
从测试的角度来说，GetNumberOfStudent2的conn可以换成mock conn，
而GetNumberOfStudent1因为conn的实例无法修改，所以无法使用gomock

由此可见，在go的代码中，不应该使用全局变量储存struct。
比如数据库连接池的使用中，连接池应该是某些需要查询数据库的struct的单例模式下的成员变量，
而不应该成为一个全局变量，否则很难使用gomock进行单元测试。
