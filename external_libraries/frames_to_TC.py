# SOURCE:
# https://gist.github.com/schiffty/c838db504b9a1a7c23a30c366e8005e8

def frames_to_TC (frames):
    h = int(frames / 86400) 
    m = int(frames / 1440) % 60 
    s = int((frames % 1440)/24) 
    f = frames % 1440 % 24
    return ( "%02d:%02d:%02d:%02d" % ( h, m, s, f))


# Breakdown of the steps above:
# Hours: Divide frames by 86400 (# of frames in an hour at 24fps). Round down to nearest integer.
# Minutes: Divide frames by 1440 (# of frames in a minute). This gives you the total number of minutes, which might be 122 for
#          content that is 2 hours, 2 minutes, but you don't want the hours here. You're only interested in the extra 2 minutes.
#          Modulo 60 will remove all full hours and return only the remaining minutes.
# Seconds: frames % 1440 removes all full minutes and returns the number of remaining frames. 
#          Divide that by 24 to convert to seconds, and round down to nearest integer.
# Frames:  frames % 1440 removes all full minutes and returns the number of remaining frames. 
#          Take that number and modulo 24 to removes all full seconds, leaving you with the remaining # of frames.
# Lastly, take those variables and put them into a string with colons between each one.