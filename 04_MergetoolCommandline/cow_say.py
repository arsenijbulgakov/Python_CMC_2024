import cmd
import cowsay
import shlex


COW_EYES = ["==", "XX", "$$", "@@", "**", "--", "OO"]
COW_TONGUES = ["U ", " U", "UU"]


class CowSay(cmd.Cmd):
    """It's cowsay shell!"""
    prompt = "cowsay$ "

    def _parse_args(self, args):
        lst = shlex.split(args)

        message = "hello!"
        cow = "default"
        eyes = "oo"
        tongue = "  "

        prev_option = False
        for idx, s in enumerate(lst):
            if s == "-f":
                cow = lst[idx+1]
                prev_option = True
            elif s == "-e":
                eyes = lst[idx+1]
                prev_option = True
            elif s == "-T":
                tongue = lst[idx+1]
                prev_option = True
            elif prev_option == False:
                message = " ".join(lst[idx:])
                break
            else:
                prev_option = False

        kwargs = {"message": message, "cow": cow, "eyes": eyes, "tongue": tongue}
        return kwargs


    def do_cowsay(self, args):
        """
        Returns the resulting cowsay string
        :param message: The message to be displayed
        :param cow: -f – the available cows can be found by calling list_cows
        :param eyes: -e – eye_string
        :param tongue: -T – tongue_string
        """
        kwargs = self._parse_args(args)
        print(cowsay.cowsay(**kwargs))


    def do_cowthink(self, args):
        """
        Returns the resulting cowthink string
        :param message: The message to be displayed
        :param cow: -f – the available cows can be found by calling list_cows
        :param eyes: -e – eye_string
        :param tongue: -T – tongue_string
        """
        kwargs = self._parse_args(args)
        print(cowsay.cowthink(**kwargs))


    def do_list_cows(self, args):
        """Lists all cow file names"""
        print(cowsay.list_cows())


    def do_make_bubble(self, message):
        """This is the text that appears above the cows"""
        if not message:
            message = "hello"
        print(cowsay.make_bubble(message))


    def do_EOF(self, arg):
        return 1


    def _get_info_for_complete(self, text, line, begidx, endidx):
        words = (line[:endidx]).split()
        
        if words[-1] == "-e":
            return COW_EYES
        elif words[-1] == "-f":
            return cowsay.list_cows()
        elif words[-1] == "-T":
            return COW_TONGUES


    def complete_cowsay(self, text, line, begidx, endidx):
        return self._get_info_for_complete(text, line, begidx, endidx)


    def complete_cowthink(self, text, line, begidx, endidx):
        return self._get_info_for_complete(text, line, begidx, endidx)


if __name__ == "__main__":
    CowSay().cmdloop()
