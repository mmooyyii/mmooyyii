package string2

import (
	"gitlab.geinc.cn/services/go-common-module/data_structure/deque"
	"gitlab.geinc.cn/services/go-common-module/utils"
	"math"
)

const (
	prime = 16777619
	mod   = math.MaxUint32
)

type RabinKarp struct {
	hash   uint64
	buffer *deque.Deque
}

func NewRabinKarp() *RabinKarp {
	return &RabinKarp{
		hash:   0,
		buffer: deque.NewDeque(),
	}
}

func (r *RabinKarp) Bytes() []byte {
	return r.buffer.ToList()
}

func (r *RabinKarp) PopLeft() *RabinKarp {
	if r.buffer.Len() == 0 {
		panic("Pop empty")
	}
	c := r.buffer.PopLeft()
	r.hash += mod - utils.Pow(prime, uint64(r.buffer.Len()), uint32(mod))*uint64(c)%mod
	r.hash %= mod
	return r
}

func (r *RabinKarp) AppendRight(c byte) *RabinKarp {
	r.hash = ((r.hash * prime) + uint64(c)) % mod
	r.buffer.AppendRight(c)
	return r
}

func (r *RabinKarp) Hash() uint64 {
	return r.hash
}

func (r *RabinKarp) SetUp(a []byte) *RabinKarp {
	r.Clear()
	for _, v := range a {
		r.AppendRight(v)
	}
	return r
}

func (r *RabinKarp) Clear() *RabinKarp {
	r.buffer.Clear()
	r.hash = 0
	return r
}

func (r *RabinKarp) MoveRight(c byte) *RabinKarp {
	r.AppendRight(c)
	r.PopLeft()
	return r
}

type ScanHash struct {
	Hash  uint64
	Left  int
	Right int
}

func Scan(text []byte, windowSize int) []ScanHash {
	if windowSize > len(text) {
		return []ScanHash{}
	}
	ans := make([]ScanHash, len(text)-windowSize+1)
	rk := NewRabinKarp()
	rk.SetUp(text[:windowSize])
	ans[0] = ScanHash{Hash: rk.Hash(), Left: 0, Right: windowSize}
	for left, right := 0, windowSize; right < len(text); left, right = left+1, right+1 {
		rk.MoveRight(text[right])
		ans[left+1] = ScanHash{Hash: rk.Hash(), Left: left + 1, Right: right + 1}
	}
	return ans
}
