#include <cstdio>
#include <iostream>
#include <vector>
#include <set>
#include <map>
#include <algorithm>
using namespace std;
int n,m ;
class job
{
	public:
		vector <int> in_state ;
		int id ;
		long long in_time ;
	/*bool  operator<(const job &a) const
	{
		if(in_time!= a.in_time)
			return in_time<a.in_time ;
		return id < a.id ;
	}*/
};
vector <job> all_jobs;
class workstation
{
	public:
	vector<int> jobs ;
	long long finish_time ;
	int id ;
	void calculate()
	{
		finish_time=0 ;
		for(unsigned int i=0;i<jobs.size();i++)
			if(finish_time < (all_jobs[jobs[i]].in_time))
				finish_time= (all_jobs[jobs[i]].in_time)+(all_jobs[jobs[i]].in_state)[id] ;
			else 
				finish_time+=(all_jobs[jobs[i]].in_state)[id] ;
			
	}
	void add_job(int job_id)
	{
		int i=0 ;
		while (i<jobs.size() && (all_jobs[jobs[i]].in_time) < (all_jobs[job_id].in_time) ) i++ ;
		jobs.insert(jobs.begin()+i,job_id) ;
		calculate() ;
	//	cout<<job_id<<" "<<*(jobs.begin()+i) <<endl ;
	}
	void del_job(int id)
	{
		int i=0 ;
		while (jobs[i] !=id && i<jobs.size()) i++ ;
		if(i!=jobs.size())
			jobs.erase(jobs.begin()+i) ;
		calculate() ;
	}
	
};
class state
{
	public:
	vector <workstation> workstations ;
	vector <int> uncalculated ;
	vector <int> where_job ;
	long long finish_time ;
	void calculate()
	{
		finish_time=0 ;
		for (unsigned int i=0;i<workstations.size();i++)
			finish_time=max(finish_time,workstations[i].finish_time) ;
	}
	void add_job(int id_workstation,int id_job)
	{
		int i=0 ;
		while (i<uncalculated.size() && uncalculated[i] !=id_job) i++ ;
		if(i!=uncalculated.size())
		{//	puts("state:add_job:1") ;
		//	cout<<	*(uncalculated.begin()+i) <<" "<<id_job<<endl ;
			uncalculated.erase(uncalculated.begin()+i) ;
		//	puts("state:add_job:2") ;	
			workstations[id_workstation].add_job(id_job) ;
		//	puts("state:add_job:3") ;
			where_job[id_job]=id_workstation ;
		//	puts("state:add_job:4") ;
		}
		//calculate() ;
		if(uncalculated.empty())
			calculate() ;
	}
	void del_job(int id_job)
	{
		int id_workstation=where_job[id_job] ;
		
		if(id_workstation!=-1)
		{	
			uncalculated.push_back(id_job) ;
			workstations[id_workstation].del_job(id_job) ;
			where_job[id_job]=-1 ;
		}
	}
	state()
	{
		workstations.resize(m) ;
		where_job.resize(n,-1) ;
		for(int i=0;i<n;i++)
			uncalculated.push_back(i) ;
		for(int i=0;i<m;i++)
			workstations[i].id=i ;
	}
	state(const state &a)
	{
		this->workstations=a.workstations ;
		this->uncalculated=a.uncalculated ;
		this->where_job=a.where_job ;
	}
	bool  operator<(const state &a) const
	{
		if(finish_time!= a.finish_time)
			return finish_time<a.finish_time ;
		return where_job < a.where_job ;
	}
};
state minimal ;
void bruteforce_rec(state new_state,int job_id) 
{
	if(job_id==n)
	{
		new_state.calculate() ;
		minimal=min(minimal,new_state) ;
	}
	else
		for(int i=0;i<m;i++)
		{
			state v=new_state ;
		//	cout<<job_id<<" 1 "<<new_state.where_job[0]<< " "<<new_state.where_job[1]<<endl ;

			v.add_job(i,job_id) ;
			bruteforce_rec(v,job_id+1); 
		}
	
}
void bruteforce()
{
	state w ;
	minimal=w ;
	minimal.finish_time=(long long)1e15 ;

	bruteforce_rec(minimal,0) ;

}
void input()
{
	cin>>n>>m ;
	for(int i=0;i<n;i++)
	{
		job new_job ;
		new_job.id=i ;
		cin>>new_job.in_time ;
		for(int i=0,v;i<m;i++)
		{
			cin>>v ;
			new_job.in_state.push_back(v) ;
		}
		all_jobs.push_back(new_job) ;
	}
}
int main()
{
	input() ;
	bruteforce() ;
	cout<<minimal.finish_time ;

}
