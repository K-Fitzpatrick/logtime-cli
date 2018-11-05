import unittest
import logtime_cli.logfile_notes_data as logfile_notes_data


class Test_Notes(unittest.TestCase):
    def test_basic_notes(self):
        test_notes = '\n'.join([
            "First line",
            "",
            "Third line",
            "Fourth line",
            "",
        ])
        notes = logfile_notes_data.LogfileNotesSection(name='Notes:', full_text=test_notes)

        self.assertEqual(notes.get_text(), test_notes)
        self.assertEqual(notes.full_text, test_notes)
        self.assertEqual(len(notes.get_subsections()), 0)

    def test_single_layer(self):
        test_notes = '\n'.join([
            "First line",
            "## Section",
            "line",
            "## Section",
            "line",
            "",
        ])
        notes = logfile_notes_data.LogfileNotesSection(name='Notes:', full_text=test_notes)
        self.assertEqual(notes.full_text, test_notes)
        self.assertEqual(notes.get_text(), "First line")
        self.assertEqual(len(notes.get_subsections()), 2)

        sections = notes.get_subsections()

        self.assertEqual(sections[0].name, "Section")
        self.assertEqual(sections[0].full_text, "line")
        self.assertEqual(sections[0].get_text(), "line")

        self.assertEqual(sections[1].name, "Section")
        self.assertEqual(sections[1].full_text, "line\n")
        self.assertEqual(sections[1].get_text(), "line\n")

    def test_nested_sections(self):
        test_notes = '\n'.join([
            "## Section1.0",
            "line1.0",
            "### Section1.1",
            "line1.1",
            "## Section2.0",
            "line2.0",
            "### Section2.1",
            "line2.1",
        ])
        notes = logfile_notes_data.LogfileNotesSection(name='Notes:', full_text=test_notes)
        self.assertEqual(notes.full_text, test_notes)
        notes_sections = notes.get_subsections()
        self.assertEqual(len(notes_sections), 2)

        section1 = notes_sections[0]
        self.assertEqual(section1.name, 'Section1.0')
        self.assertEqual(section1.full_text,
                         '\n'.join([
                             "line1.0",
                             "### Section1.1",
                             "line1.1",
                         ])
                        )
        self.assertEqual(section1.get_text(), 'line1.0')
        section1_sections = section1.get_subsections()
        self.assertEqual(len(section1_sections), 1)
        self.assertEqual(section1_sections[0].name, 'Section1.1')
        self.assertEqual(section1_sections[0].full_text, 'line1.1')
        self.assertEqual(section1_sections[0].get_text(), 'line1.1')

        section2 = notes_sections[1]
        self.assertEqual(section2.name, 'Section2.0')
        self.assertEqual(section2.full_text,
                         '\n'.join([
                             "line2.0",
                             "### Section2.1",
                             "line2.1",
                         ])
                        )
        self.assertEqual(section2.get_text(), 'line2.0')
        section2_sections = section2.get_subsections()
        self.assertEqual(len(section2_sections), 1)
        self.assertEqual(section2_sections[0].name, 'Section2.1')
        self.assertEqual(section2_sections[0].full_text, 'line2.1')
        self.assertEqual(section2_sections[0].get_text(), 'line2.1')


    def test_deeply_nested_sections(self):
        test_notes = '\n'.join([
            "## Section1",
            "### Section2",
            "#### Section3",
            "##### Section4",
            "line",
        ])
        notes = logfile_notes_data.LogfileNotesSection(name='Notes:', full_text=test_notes)
        self.assertEqual(notes.full_text, test_notes)
        self.assertEqual(len(notes.get_subsections()), 1)

        section1 = notes.get_subsections()[0]
        self.assertEqual(section1.name, 'Section1')
        self.assertEqual(section1.full_text,
                         '\n'.join([
                             "### Section2",
                             "#### Section3",
                             "##### Section4",
                             "line",
                         ])
                        )
        self.assertEqual(section1.get_text(), '')
        self.assertEqual(len(section1.get_subsections()), 1)

        section2 = section1.get_subsections()[0]
        self.assertEqual(section2.name, 'Section2')
        self.assertEqual(section2.full_text,
                         '\n'.join([
                             "#### Section3",
                             "##### Section4",
                             "line",
                         ])
                        )
        self.assertEqual(section2.get_text(), '')
        self.assertEqual(len(section2.get_subsections()), 1)

        section3 = section2.get_subsections()[0]
        self.assertEqual(section3.name, 'Section3')
        self.assertEqual(section3.full_text,
                         '\n'.join([
                             "##### Section4",
                             "line",
                         ])
                        )
        self.assertEqual(section3.get_text(), '')
        self.assertEqual(len(section3.get_subsections()), 1)

        section4 = section3.get_subsections()[0]
        self.assertEqual(section4.name, 'Section4')
        self.assertEqual(section4.full_text, 'line')
        self.assertEqual(section4.get_text(), 'line')
        self.assertEqual(len(section4.get_subsections()), 0)

if __name__ == '__main__':
    unittest.main()
