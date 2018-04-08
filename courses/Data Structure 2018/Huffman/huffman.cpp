/*
 * huffman.cpp
 *
 *  Created on: 2018年4月2日
 *      Author: pc39
 */


#include <iostream>
#include <stdlib.h>
#include <string>
#include <algorithm>
#include <queue>
#include <functional>
using namespace std;

typedef struct{
	char data;
	int fre;
}precode;

typedef struct{
	char data;
	string code;
}cipher;

int getf(char data,precode* pre,int num);
bool isoverlap(cipher* codes,int num);
bool cmp(cipher code1,cipher code2);

int main(){
	int num;
	cin>>num;
	precode* pre = new precode[num];
	priority_queue<int, vector<int>, greater<int>> q;
	for (int i=0;i<num;i++){
		cin>>(pre+i)->data;
		cin>>(pre+i)->fre;
		q.push((pre+i)->fre);
	}
	int sum;
	int leastcost=0;
	if (q.size()>1){
	while(q.size()>1){

			sum = q.top();
			q.pop();
			sum+=q.top();
			q.pop();
			q.push(sum); /*统计非叶子节点和值*/
		    leastcost+=sum; /*每次的堆顶元素相加*/
	}
}
	else
		leastcost = q.top();
	/* now, check*/

	int N;
	cipher* codes=new cipher[num];
	cin>>N;
	/* N students submitted results, so check N times!*/
	for(int i=0;i<N;i++){
		int cost = 0;
		/* 接受一次输入*/
		for (int j=0;j<num;j++){
			cin>>(codes+j)->data;
			cin>>(codes+j)->code;
		}
		/*compute cost*/
		for(int j=0;j<num;j++)
			cost+=(codes+j)->code.size()*getf((codes+j)->data,pre,num);
		/*cost too much?? No!*/
		if (cost>leastcost)
			cout<<"No"<<endl;
		/*cost right but not distinguishable?? No!*/
		else if (isoverlap(codes,num))
				cout<<"No"<<endl;
		else
				cout<<"Yes"<<endl;
		}
	return 0;
	}



int getf(char data,precode* pre,int num){
	for (int i=0;i<num;i++){
		if (data==(pre+i)->data)
			return (pre+i)->fre;
	}
	return 0;
}

bool isoverlap(cipher* codes, int num){
	sort(codes,codes+num,cmp);
	for(int i=0;i<num-1;i++){
		string tmp = (codes+i)->code;
		for (int j=i+1;j<num;j++){
			if(tmp==(codes+j)->code.substr(0,tmp.size()))
				return true;
		}
	}
	return false;
}

bool cmp(cipher code1, cipher code2){
	/*code1 and code2 are pointers, so use "." instead of "->"*/
	return code1.code.size()<code2.code.size();
}
