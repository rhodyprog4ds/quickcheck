import click 
import nbformat

# settings 
# tolerance on consecutive cells of one type
streak_limit = 3
# 
cm_ratio_lb = .8

@click.command()
@click.argument(file)

def check_for_narrative(file):
    '''
    check a notebook file for a balance of code and narrative
    '''
    submission = nbformat.read(file, as_version=4)

    
    cell_types = [s.cell_type for s in submission.cells]

    type_counts = {st:cell_types.count(st) for st in set(cell_types)}

    ratio = type_counts['markdown']/type_counts['code']
    ratio_message = {-1:'you have a lot more code cells than markdown cells',
                    0:'you have a good ratio of code to markdown',
                    1:'you have a lot more markdown than code cells'}

    click.echo(ratio_message[(ratio<cm_ratio_lb)*-1 + (ratio>1.2)*1])

    streak =0
    max_streak = 0
    prev = cell_types[0]
    streak_type =prev
    for ct in cell_types[1:]:
        cur = int(ct == prev)
        streak = streak*cur +cur
        # flip these if greater, otherwise keep the same
        max_streak = (streak>max_streak)*streak + (streak<max_streak)*max_streak
        streak_type = (streak>=max_streak)*ct + (streak<max_streak)*streak_type
        prev = ct

    streak_message = {True:'you have a streak of {count} consecutive {ctype} cells'.format(
                                                        count=max_streak,ctype=streak_type),
                    False:'your code & markdown cells are interspersed well'}

    click.echo(streak_message[max_streak>streak_limit])

    # check for short markdown cells that are not headers 
    header_state = [c['source'][0]=='#' for c in sub.cells if c['cell_type']=='markdown']
    wc = [len(c['source'].split()) for c in sub.cells if c['cell_type']=='markdown']
    num_short = sum([not(w>10 or h) for w, h in zip(wc,header_state)])
    if num_short:
        click.echo('you have '+ str(num_short) + 
                                        ' short markdown cells that are not headers')

    header_rate = int(sum(header_state)/type_counts['markdown']*100)
    if header_rate>20:
        click.echo(str(header_rate)+ '% of your markdown cells are headers' )


    # check if cells were last run in order 
    ec = [c['execution_count'] for c in submission.cells if c['cell_type']=='code']
    ecc = [e for e in ec if e]
    
    sorted(ecc) ==ecc

    # check loop variables 
    loops = [loopre for loopre in [re.search('for . in',c['source']) 
                    for c in submission.cells if c['cell_type']=='code'] if loopre]
    click.echo('you have ' + len(loops) + ' loops or comprehensions with single character variables')



