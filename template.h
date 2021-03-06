#include <iostream>
#include <vector>

using namespace std;

template <typename T>
void SHOWANY(vector<string> name, T t) {
    cout << name.front() << " = " << t << endl;
}
template<typename T, typename... Args>
void SHOWANY(vector<string> name, T t, Args... args) {
    cout << name.front() << " = " << t << ", ";
    name.erase(name.begin());
    SHOWANY(name, args...);
}

vector<string> split_name(string name) {
	// does not support string ""
	vector<string> n;
	bool following_comma = false;
	int bracket = 0;
	int l = 0;
	int r = 0;
	for ( ; r < name.length(); r++) {
		char cur = name[r];
		if (cur == '(')
			bracket++;
		if (cur == ')')
			bracket--;
		if (bracket)
			continue;
		if (cur == ',') {
			n.push_back(name.substr(l, r - l));
			l = r + 1;
			following_comma = true;
		}
		else if (cur == ' ' && following_comma)
			l = r + 1;
		else
			following_comma = false;
	}
	n.push_back(name.substr(l, r - l));
	return n;
}


#ifdef SHOW
#undef SHOW
#endif

#ifdef REACH_HERE
#undef REACH_HERE
#endif

#ifdef PRINT
#undef PRINT
#endif

#ifdef PRINTLN
#undef PRINTLN
#endif

#define SHOW(...) { SHOWANY(split_name(#__VA_ARGS__), __VA_ARGS__); }
#define REACH_HERE { cout << "REACH_HERE! line " << __LINE__ << endl; }
#define PRINT(s, ...) { printf(s, ##__VA_ARGS__); } 
#define PRINTLN(s, ...) { printf(s, ##__VA_ARGS__); printf("\n"); } 
// 
// http://codecraft.co/2014/11/25/variadic-macros-tricks/
// 

