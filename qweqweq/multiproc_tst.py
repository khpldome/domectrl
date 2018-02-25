

import multiprocessing


def worker(num, cmd):
    """worker function"""
    print('Worker', num, cmd)

    return


if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(i, 'cmd',))
        jobs.append(p)
        p.start()




    print(jobs)



