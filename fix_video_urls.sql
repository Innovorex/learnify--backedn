-- Fix Video URLs with Working YouTube Videos
-- Run this SQL to update broken video URLs

-- Module 1: Childhood and Growing Up
UPDATE module_topics SET video_url = 'https://www.youtube.com/embed/GlJxbqIshxQ' WHERE topic_number = 1 AND topic_name = 'Introduction to Child Development';
UPDATE module_topics SET video_url = 'https://www.youtube.com/embed/TRF27F2bn-A' WHERE topic_number = 2 AND topic_name = 'Theories of Development - Piaget';
UPDATE module_topics SET video_url = 'https://www.youtube.com/embed/8dGcT5LeMoQ' WHERE topic_number = 3 AND topic_name = 'Vygotsky''s Sociocultural Theory';
UPDATE module_topics SET video_url = 'https://www.youtube.com/embed/hiduiTq1ei8' WHERE topic_number = 4 AND topic_name = 'Adolescent Psychology';
UPDATE module_topics SET video_url = 'https://www.youtube.com/embed/HFEt038wqBY' WHERE topic_number = 5 AND topic_name = 'Learning Styles and Individual Differences';

-- Module 2: Contemporary India and Education
UPDATE module_topics SET video_url = 'https://www.youtube.com/embed/aPHCGQR2D0s' WHERE topic_name = 'Indian Education System Overview';
UPDATE module_topics SET video_url = 'https://www.youtube.com/embed/zDZFcDGpL4U' WHERE topic_name = 'Right to Education Act (RTE)';
UPDATE module_topics SET video_url = 'https://www.youtube.com/embed/jJDBQgKnNuE' WHERE topic_name = 'National Education Policy 2020';

-- Module 3: Learning and Teaching
UPDATE module_topics SET video_url = 'https://www.youtube.com/embed/lI85ap8J-P8' WHERE topic_name = 'Theories of Learning';
UPDATE module_topics SET video_url = 'https://www.youtube.com/embed/eVtCO84MDj8' WHERE topic_name = 'Constructivist Approach to Teaching';

-- Module 4: Curriculum and Inclusion
UPDATE module_topics SET video_url = 'https://www.youtube.com/embed/6M9E3z3pGkE' WHERE topic_name = 'Curriculum Development';
UPDATE module_topics SET video_url = 'https://www.youtube.com/embed/6JB0_IRukZU' WHERE topic_name = 'Inclusive Education';

-- Module 5: Pedagogy of Mathematics
UPDATE module_topics SET video_url = 'https://www.youtube.com/embed/aircAruvnKk' WHERE topic_name = 'Nature of Mathematics';
UPDATE module_topics SET video_url = 'https://www.youtube.com/embed/hbPRaCLVcng' WHERE topic_name = 'Teaching Methods in Mathematics';
UPDATE module_topics SET video_url = 'https://www.youtube.com/embed/wKcZ8ozCah0' WHERE topic_name = 'Problem-Solving Approach';
UPDATE module_topics SET video_url = 'https://www.youtube.com/embed/R9OHn5ZF4Uo' WHERE topic_name = 'Technology in Mathematics Education';

-- Module 6: Assessment for Learning
UPDATE module_topics SET video_url = 'https://www.youtube.com/embed/iXZMfJLEy7I' WHERE topic_name = 'Formative vs Summative Assessment';
UPDATE module_topics SET video_url = 'https://www.youtube.com/embed/JUIlRW_UF2k' WHERE topic_name = 'Continuous and Comprehensive Evaluation';

-- Module 7: Educational Technology
UPDATE module_topics SET video_url = 'https://www.youtube.com/embed/d_9AFmg-mYQ' WHERE topic_name = 'ICT in Teaching-Learning';

-- Module 8: Teacher Identity and Professional Ethics
UPDATE module_topics SET video_url = 'https://www.youtube.com/embed/RCQ6l23wguo' WHERE topic_name = 'Role of Teachers in 21st Century';
UPDATE module_topics SET video_url = 'https://www.youtube.com/embed/dGCJ46vyR9o' WHERE topic_name = 'Professional Ethics and Conduct';
