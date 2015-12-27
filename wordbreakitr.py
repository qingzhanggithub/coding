def word_break(s, d):
	t=[]
	if s[0] in d:
		t.append([s[0]])
	else:
		t.append([])
	for i in range(1, len(s)+1):
		snt = []
		for j in range(i):
			cur = ''
			if s[j:i+1] in d:
				if j-1<0 or  len(t[j-1]) >0:
					cur = s[j:i+1]
					if j-1>=0:
						snt += [e + ' ' + cur for e in t[j-1]]
					else:
						snt += [cur]
			print s[:i+1], '\t', j, '-', i, '\t', s[j:i+1], '\t', snt 

		t.append(snt)
			
	print 'result\t',t[-1]


s='brandnewlaptop'
d=['brand', 'new', 'lap', 'top', 'laptop']
word_break(s, d)

