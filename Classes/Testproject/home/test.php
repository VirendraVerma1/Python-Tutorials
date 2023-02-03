public function index()
    {
        $groups=Group::join('notification_group','notification_group.group_id','group_name.id')->join('tblcompany','tblcompany.id','notification_group.customer_id')
        ->select('group_name.id','group_name.group_name','tblcompany.company_name','notification_group.customer_id')->get();
        // $member=array();
        // foreach($groups as $grp)
        // {
        //    if($grp->id)
        //    {
        //     array_push($member,$grp->customer_id);
        // }
        
        // $mem=DB::table('tblcompany')->whereIn('id',$member)->get();
        // // dd($mem);

        $unique_group_ids=array();

        foreach($groups as $g)
        {
            $flag=false;
            foreach($unique_group_ids as $ug)
            {
                if($ug->id==$g->id)
                {
                    $flag=true;
                }
            }

            if($flag==false)
            {
                array_push($unique_group_ids,$g);
            }
        }

        $unique_groups=array();
        

        foreach($unique_group_ids as $g)
        {
            $flag=false;
            $unique_company=array();
            foreach($groups as $ug)
            {
                if($ug->id as $g->id)
                {
                    array_push($unique_company,$ug->company_name);
                    $flag=true;
                }
            }
            $g->all_companies=$unique_company;

        }

        $groups=$unique_group_ids;

        return view('group.index',compact('groups'));
    }