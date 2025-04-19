import unittest
import pygame
import os

# Assuming Part-07-Objects.py is in the same directory
# Import the necessary components from the script
# Note: This will execute the image loading part of Part-07-Objects.py
try:
    # Try importing directly if run from the same directory
    from Part_07_Objects import Hero, win_width, win_height, left, right
except ImportError:
    # Handle potential path issues if run differently (less common for simple cases)
    print("Error: Ensure test_hero.py is in the same directory as Part_07_Objects.py")
    exit()


class TestHeroClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialize Pygame once for the test class."""
        # Pygame needs to be initialized to use its constants (like K_LEFT)
        # and potentially for surface creation if testing drawing more deeply.
        pygame.init()
        # Define a dummy display surface if needed for blitting tests
        cls.dummy_surface = pygame.Surface((win_width, win_height))


    def setUp(self):
        """Set up a fresh Hero instance before each test method."""
        self.start_x = 250
        self.start_y = 405 # Matches 270*3/2 in the original script
        self.hero = Hero(self.start_x, self.start_y)
        # Store original velocities if needed
        self.original_velx = self.hero.velx
        self.original_vely = self.hero.vely

    # --- Test Initialization (__init__) ---

    def test_initial_position(self):
        self.assertEqual(self.hero.x, self.start_x)
        self.assertEqual(self.hero.y, self.start_y)

    def test_initial_velocity(self):
        self.assertEqual(self.hero.velx, 10)
        self.assertEqual(self.hero.vely, 10) # Initial jump velocity

    def test_initial_direction(self):
        self.assertTrue(self.hero.face_right)
        self.assertFalse(self.hero.face_left)

    def test_initial_animation_state(self):
        self.assertEqual(self.hero.stepIndex, 0)

    def test_initial_jump_state(self):
        self.assertFalse(self.hero.jump)

    # --- Test move_hero ---

    def _get_mock_input(self, left_pressed=False, right_pressed=False, space_pressed=False):
        """Helper to create a mock userInput dictionary."""
        # Simulate pygame.key.get_pressed() which returns a sequence/list
        # Using a dictionary for clarity in tests
        mock = {pygame.K_LEFT: 0, pygame.K_RIGHT: 0, pygame.K_SPACE: 0}
        if left_pressed:
            mock[pygame.K_LEFT] = 1
        if right_pressed:
            mock[pygame.K_RIGHT] = 1
        if space_pressed:
            mock[pygame.K_SPACE] = 1
        return mock

    def test_move_right(self):
        mock_input = self._get_mock_input(right_pressed=True)
        initial_x = self.hero.x
        self.hero.move_hero(mock_input)
        self.assertEqual(self.hero.x, initial_x + self.hero.velx)
        self.assertTrue(self.hero.face_right)
        self.assertFalse(self.hero.face_left)

    def test_move_left(self):
        mock_input = self._get_mock_input(left_pressed=True)
        initial_x = self.hero.x
        self.hero.move_hero(mock_input)
        self.assertEqual(self.hero.x, initial_x - self.hero.velx)
        self.assertFalse(self.hero.face_right)
        self.assertTrue(self.hero.face_left)

    def test_no_horizontal_move_resets_stepIndex(self):
        # Move first to ensure stepIndex might not be 0
        self.hero.move_hero(self._get_mock_input(right_pressed=True))
        self.hero.stepIndex = 5 # Manually set stepIndex
        mock_input = self._get_mock_input() # No keys pressed
        initial_x = self.hero.x
        self.hero.move_hero(mock_input)
        self.assertEqual(self.hero.x, initial_x) # Position shouldn't change
        self.assertEqual(self.hero.stepIndex, 0) # stepIndex should reset

    def test_move_right_boundary(self):
        self.hero.x = win_width - 62 # At the boundary
        mock_input = self._get_mock_input(right_pressed=True)
        self.hero.move_hero(mock_input)
        self.assertEqual(self.hero.x, win_width - 62) # Should not move past boundary

    def test_move_left_boundary(self):
        self.hero.x = 0 # At the boundary
        mock_input = self._get_mock_input(left_pressed=True)
        self.hero.move_hero(mock_input)
        self.assertEqual(self.hero.x, 0) # Should not move past boundary

    # --- Test jump_motion ---

    def test_start_jump(self):
        self.assertFalse(self.hero.jump)
        mock_input = self._get_mock_input(space_pressed=True)
        self.hero.jump_motion(mock_input)
        self.assertTrue(self.hero.jump)

    def test_no_jump_if_already_jumping(self):
        self.hero.jump = True
        self.hero.vely = 5 # Mid-jump
        mock_input = self._get_mock_input(space_pressed=True)
        self.hero.jump_motion(mock_input)
        self.assertTrue(self.hero.jump) # Should still be jumping
        self.assertEqual(self.hero.vely, 4) # Velocity should decrease, not reset

    def test_jump_y_change(self):
        self.hero.jump = True
        initial_y = self.hero.y
        initial_vely = self.hero.vely
        mock_input = self._get_mock_input() # No space pressed, just process jump physics
        self.hero.jump_motion(mock_input)
        self.assertEqual(self.hero.y, initial_y - (initial_vely * 4))

    def test_jump_vely_change(self):
        self.hero.jump = True
        initial_vely = self.hero.vely
        mock_input = self._get_mock_input()
        self.hero.jump_motion(mock_input)
        self.assertEqual(self.hero.vely, initial_vely - 1)

    def test_jump_completion(self):
        self.hero.jump = True
        self.hero.vely = -10 # Set velocity to the trigger point for ending jump
        mock_input = self._get_mock_input()
        self.hero.jump_motion(mock_input)
        self.assertFalse(self.hero.jump) # Jump should end
        self.assertEqual(self.hero.vely, 10) # Velocity should reset

    # --- Test draw (Focus on stepIndex logic) ---
    # We pass a dummy surface because blit requires one. We don't check the visual output.

    def test_draw_increments_stepIndex_right(self):
        self.hero.face_right = True
        self.hero.face_left = False
        initial_index = self.hero.stepIndex
        self.hero.draw(self.dummy_surface)
        self.assertEqual(self.hero.stepIndex, initial_index + 1)

    def test_draw_increments_stepIndex_left(self):
        self.hero.face_right = False
        self.hero.face_left = True
        initial_index = self.hero.stepIndex
        self.hero.draw(self.dummy_surface)
        self.assertEqual(self.hero.stepIndex, initial_index + 1)

    def test_draw_resets_stepIndex_at_limit(self):
        self.hero.stepIndex = 8 # One before the limit (9 frames, indices 0-8)
        self.hero.face_right = True # Ensure it tries to draw moving
        self.hero.draw(self.dummy_surface)
        self.assertEqual(self.hero.stepIndex, 0) # Should wrap around from 9 to 0

    # Note: The original draw method increments stepIndex if face_left OR face_right.
    # If somehow both were true, it would increment twice. This test reflects that.
    def test_draw_increments_stepIndex_twice_if_both_flags_set(self):
        # This state shouldn't happen with current move_hero, but tests draw() in isolation
        self.hero.face_right = True
        self.hero.face_left = True
        initial_index = self.hero.stepIndex
        self.hero.draw(self.dummy_surface)
        # It blits left[index], increments, then blits right[index+1], increments again
        self.assertEqual(self.hero.stepIndex, initial_index + 2)


    @classmethod
    def tearDownClass(cls):
        """Quit Pygame once after all tests are done."""
        pygame.quit()

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    # Using argv and exit=False makes it friendlier if run in some IDEs/notebooks
    # You can also just use: unittest.main()
