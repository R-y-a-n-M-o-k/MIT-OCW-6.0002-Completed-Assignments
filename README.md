These are solutions to the MIT OpenCourseWare 6.0002 course (Introduction to Computational Thinking and Data Science)

Many of the course materials (original .py files, images, data) are originally from Massachusetts Institute of Technology and are available through MIT OpenCourseWare.

- Some changes were made to ps5_test.py in order to make the code run. self.assertEquals was changed to self.assertEqual. In the original, suite.addTest(unittest.makeSuite(TestPS5)) was used but this did not seem to be functional any longer. This was instead replaced with suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPS5)).

This repository contains my own work unless otherwise noted and is not affiliated with or endorsed by MIT.