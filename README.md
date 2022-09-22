# GGPLOT Assignment

##### Brendon Stanley
##### STAA 566

# Introduction
When I was 15 I build my first speaker for a high school physics project. Soldered the amplifier from a kit, teacher helped
me design the crossover network (circuity that tells high frequency to be played on the tweeter, bass on the big woofers), and
my dad helped me build the speaker boxes. 

It sounded terrible ... 

I then failed the exam on circuits ...

... so naturally I went college for electrical engineering.

Much to the dismay of many a neighbor I kept building speakers. Big ones, small ones, massive subwoofers that
can find the resident frequency of your house. I may not be a musician - but friends always seemed to find the rhythm
dancing at my home.

Back in high school my physics always said that when he retired his goal was to start a speaker company and make the best
audio gear in Colorado. A few months ago I got a beer with my former teacher. It's his year teaching, and he has in fact
started his speaker company!

Right now I have the second-smallest model. They stand at just over five feet tall and weigh 175lb. Each.

For this assignment I would like to test just how good my teachers speakers are.

# Problem Statement
In any movie theater speaker setup the most important speakers are the left, center, and right (LCR) channels. At a movie theater they sit behind the screen 
(the screens are acoustically transparent - i.e. audio is uniformly attenuated). If you sit in a seat that is perfectly in the center of the screen then
the center channel is directly in 0 degrees off axis to you. The left and right channels would then sit ±θ degrees off axis where 13 < θ <25 degrees.

Ideally the LCR channels should be the same speaker. It allows for easier mixing of sound and produces a constant timber in the forward sound-stage.

Unfortunately, I do not have the budget of a high-end movie theater and so compromises where made. While the Left and Right channels I 
purchased from my former physics are identical the center channel was a modified design to cut costs.

The left and right channels use a 2.5 way design.
- the tweeter plays frequencies higher than 800Hz
- the woofer plays frequencies lower than 800 Hz
- a pair of additional woofers play frequencies lower than 80 Hz (for the kick drum in your chest feel)
- tweeter is a 39 ribbon tweeter

> Note: a ribbon tweeter is conductive material, typically in a rectangular shape, that is suspended in a permanent magnetic field. 
> When an AC single is ran across the conductive material it will create an inductive magnetic field and the entire conductive structure will 
> then be pulled to or from permanent magnetic field pending the changing polarity of the AC single. 
> This causes the structure to oscillate in time with the audio single and creating a sound wave. 
> This is more comparable to how human vocal cords produce sound compared to a traditional dome speaker.

The center channel on the other hand is a modified 2 way design:
- the tweeter plays frequencies higher than 1000Hz
- the woofer plays frequencies lower than 1000 Hz (woofer is the same)
- tweeter is a 29 ribbon tweeter

So there are two main "bad things" happening here:
- The center channel's tweeter has 25% less surface area than its left-right counterparts (the center of all three tweeters is the same height)
- the cross-over frequency has been increased in compensate for the reduced output from the smaller twitter.

For this assignment I will compare the left-right channel design to the center channel.

# What We Are Going To Measure (and then plot)
One of the most fundamental ways to measure the "goodness" of a speaker is its frequency response. Simply put give a speaker an input playing
frequencies across the human hearing range from 20Hz-20kHz and measure the output with a microphone. Plot input frequency on the X-axis and the
resulting speaker volume on the Y-axis as a measure of dB.

Standard practice is to measure a speaker directly in front (0 degrees off axis) at one meter. It is not always that a listener will be
directly in front of a speaker so measurements should also betake at various off-axis point one meter way. This will measure how listeners
to the left and right, outside the "sweet spot", will hear the sound. A good speaker will have a wide sweet spot so everyone hears the same thing.

I will measure:
- right speaker and the center speaker
- at off-axes degrees: 0, 15, 30, 45
- computer will output a while noise WAV file at 44.1Hz at 16bit depth (CD quality) for 1 second
- External digital-to-analog (DAC) converter will decode WAV and provide input to power amplifier
- microphone will be at ear level (based on my ear)
- microphone will be one meter way from the center of the speaker
- microphone will record in mono at 44.1Hz at 16bit depth (CD quality)

> Note: White noise is uniform power density across the spectrum - i.e. the FFT of 20Hz-20kHz is uniform from 20Hz-20kHz.

> Note: Typically, it is good to measure both horizontal and vertical off axis response. As I assume a "listener" will be seated on my couch I will
> not measure vertical off-axes response.

> Note: High frequencies are attenuated first. So expect that in the results. Think back to the last time a car with a souped up sound system drive past
> or the last time you went to a concert. The first thing you heard coming was the frequency bass.

> Note: Ribbon tweeters are notorious for having terrible off-axis response. Typically, at a concert or movie theater titanium drivers are used in a waveguide
> that directs the sound as it leaves - much the same way the horn of a trumpet directs sounds. This creates a good off axis response that is also *highly* efficent
> to power. Allowing concert levels of volume that make most people, who are not in the nose bleed seats, happy.

-> Final Note: I just moved so I cannot find my good calibration mic. I will be using something much cheaper - so data will have lots of noise.

# Source Data
The data used for this assignment was generated by the two supporting Python files in this Repo.

`record_audio_sample.py`
- outputs test white noise (via default system output) to speakers (I have a fancy DAC hooked and a beefy power amplifier hooked up to reduce distortion in the audio chain)
- while audio single is being played from speakers stream system's default audio input to a .wav file
- i.e. it plays a sound and record what your microphone picks up

`process_fft.py`
- reads in a collection of WAV files
- performs fft on each file
- saves fft to new csv. Each column is the fft displaying 20Hz-20kHz for each .wav file inputted

Between these Python files the raw data is generated and preprocessed for the assignment.

# Where are important Files?

- R Markdown Report can be found at `../ggplot2-brendo61-byte/r_report.pdf`
- The R code is at `../ggplot2-brendo61-byte/R_Studio/ggplot_hw.rmd`
- Python code is found under `../ggplot2-brendo61-byte/Python`
- Readers can find the raw WAV files at `../ggplot2-brendo61-byte/speaker_samples`
- The FFT files are can be found at `../ggplot2-brendo61-byte/fft_data`

# Conclusion

For these speakers being in an unfinished basement their response is rather good. For both speakers it can be seen that there is some
instability around the cross-over point and this is to be expected. Center channel has a wider amplitude in the 4kHz-10kHz range while in the
same band the right channel is very linear. Both speakers begin dropping past 10kHz a more aggressively then desired.

Overall both speakers designs show solid frequency responses and will within tolerance for proper digital EQ to fix.
