import TETRIS2_aux as aux
def score_rc(layed):
    rows = [[False for y in range(0,10)] for x in range(0, 20)]
    rows_counter = [0 for x in range(0, 20)]
    for x, y in layed:
        rows[int(y)][int(x)] = True
        
    for yy, y in enumerate(rows): 
        for x in y:
            if x:
                rows_counter[yy] += 1

    for x in rows_counter[:]:
        rows_counter[rows_counter.index(x)] = 10 - rows_counter[rows_counter.index(x)]

    for x in rows_counter[:]:
        if x == 10:
            rows_counter.remove(x)
        else:
            rows_counter[rows_counter.index(x)] **= 2
            
    return sum(rows_counter)

def score_df(layed):
    score = []
    lay_files = [[] for x in range(0,10)]
    for x, y in layed:
        lay_files[x].append(y)
    for x in lay_files:
        if len(x) == 0:
            lay_files[lay_files.index(x)] = 0
        else:
            lay_files[lay_files.index(x)] = 20 - min(x)
    
    for xx, x in enumerate(lay_files):
        try:
            score.append(abs(x - lay_files[xx+1]))
        except:
            pass

    return sum(score)

def score_hl(layed):
    score = []
    lay_files = [[] for x in range(0,10)]
    for x, y in layed:
        lay_files[x].append(int(19 - y))
    
    for x in lay_files:
        try:
            complete = [z for z in range(0, max(x)+1)]
            score.append(len(complete) - len(x))
        except:
            score.append(0)
            
    return sum(score)
        
def score_he(layed):
    lay_files = [[] for x in range(0,10)]
    for x, y in layed:
        lay_files[x].append(y)
    for x in lay_files:
        if len(x) == 0:
            lay_files[lay_files.index(x)] = 0
        else:
            lay_files[lay_files.index(x)] = 20 - min(x)
        
    return max(lay_files)
      
def layed_form(layed, complx):
    nu = []
    if complx:
        for y in layed:
            nu.append((y, "black"))
    else:
        for y in layed:
            nu.append(y[0])
            
    return nu

def get_keys(active, saved, layed_complx):
    ss, aa, dd, qq, ee, ssp = [x*0 for x in range(0, 6)]
        
    limit_save = []
    scoreboard = []
    for ii, i in enumerate((active, saved)):
        if i == None:
            continue
        scoreboard.append([])
        for r in range(0,4):
            scoreboard[ii].append([])
            i.rotate = r
            i.refr()
            
            i_rot_x = [x[0] for x in i.rot]
            limits = [abs(min(i_rot_x)), 10 - max(i_rot_x)]
            limit_save.append(tuple(limits))
            for x in range(*limits):
                # layed_save = layed
                i.pos = [x, 2]
                layed_complx_save = layed_complx
                falling = True
                while falling:
                    i.pos[1] += .5
                    if i.pos[1] > 30:
                        print("el pepe")
                    if i.check_colision(layed_complx):
                        falling = False
                        layed = layed_form(layed_complx, False)
                        
                        for y in i.rot:
                            layed.append((i.pos[0]+y[0], (i.pos[1]+y[1])//1))

                        n_rows = 0
                        layed = layed_form(layed, True)
                        for y in range(0,4):
                            layed, n = aux.full_line(layed)
                            n_rows += n
                        match n_rows:
                            case 0:
                                points = 0
                            case 1:
                                points = 100
                            case 2:
                                points = 400
                            case 3:
                                points = 2000
                            case 4:
                                points = 5000
                        
                layed_complx = layed_complx_save
                    
                layed = layed_form(aux.remove_outs(layed), False)
                s_df = score_df(layed)
                s_hl = score_hl(layed) 
                s_he = score_he(layed)
                s_rc = score_rc(layed)
                score = points*10 - s_df*100 - s_hl*1000 - (s_he**2.5)*5 - s_rc*3.5
                # print(s_df*100, s_hl*1000, (s_he**2.5)*5, s_rc*3.5)
                scoreboard[ii][r].append(score)

    # print(scoreboard)

    one_d_score = []
    score_coords = []
    for ii, i in enumerate(scoreboard):
        for rr, r in enumerate(i):
            for xx, x in enumerate(r):
                one_d_score.append(x)
                score_coords.append((ii, rr, xx))

    # print(one_d_score)
    # print(score_coords)

    ss = 1
    # try:
    if len(one_d_score)!=0:
        indx = one_d_score.index(max(one_d_score))
        # print(indx)

        ssp = score_coords[indx][0]
        qq = score_coords[indx][1]

        dd = score_coords[indx][2] + limit_save[qq][0] - 4
        if dd < 0:
            aa = abs(dd)
            dd = 0

        return ssp, aa, dd, qq, ee, ss
    # except:
    else:
        return ssp, aa, dd, qq, ee, ss