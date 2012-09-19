from django.template.base import Library, Node, TemplateDoesNotExist, TemplateSyntaxError
from django.template.defaulttags import token_kwargs
from django.template.loader import get_template
from django.template.loader_tags import BlockNode

register = Library()


class IncludeNode(Node):

    def __init__(self, template_name, resolve=False, block=None, *args, **kwargs):
        self.template_name = template_name
        self.resolve = resolve
        self.with_context = kwargs.pop("with", {})
        self.isolate = kwargs.pop("only", False)
        self.quiet = kwargs.pop("quiet", False)
        self.block = block
        super(IncludeNode, self).__init__(*args, **kwargs)

    def get_block(self, template, name):
        for node in template.nodelist.get_nodes_by_type(BlockNode):
            if node.name == name:
                return node

    def render(self, context):
        template_name = self.template_name

        if self.resolve:
            template_name = template_name.resolve(context)

        try:
            template = get_template(template_name)
        except TemplateDoesNotExist:
            if self.quiet:
                return ""
            else:
                raise

        if self.block:
            node = self.get_block(template, self.block)
            if node is None:
                if self.quiet:
                    return ""
                else:
                    raise TemplateDoesNotExist(
                        "Block %s does not exist in template %s" % (
                            self.block,
                            self.template_name,
                        )
                    )
            return node.render(context)

        return self.render_template(template, context)

    def render_template(self, template, context):
        values = dict([(name, var.resolve(context)) for name, var
           in self.with_context.iteritems()])
        if self.isolate:
            return template.render(context.new(values))
        context.update(values)
        output = template.render(context)
        context.pop()
        return output


@register.tag("include")
def partial_include(parser, token):
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("%r tag takes at least one argument: the name of the template to be included." % bits[0])

    options = {}
    remaining_bits = bits[2:]
    while remaining_bits:
        option = remaining_bits.pop(0)
        if option == "with":
            value = token_kwargs(remaining_bits, parser, support_legacy=False)
            if not value:
                raise TemplateSyntaxError('"with" in %r tag needs at least one keyword argument.' % bits[0])
        elif option == "only":
            value = True
        elif option == "quiet":
            value = True
        else:
            raise TemplateSyntaxError("Unknown argument for %r tag: %r." % (bits[0], option))
        options[str(option)] = value

    options.setdefault("only", False)
    options.setdefault("quiet", False)
    options.setdefault("with", {})

    block = options["with"].pop("block", None)
    if block:
        block = block.token
        if is_quoted(block):
            block = block[1:-1]

    template_name = bits[1]
    if is_quoted(template_name):
        resolve = False
        template_name = template_name[1:-1]
    else:
        resolve = True
        template_name = parser.compile_filter(template_name)

    return IncludeNode(template_name, resolve=resolve, block=block, **options)


def is_quoted(value):
    return value[0] in ('"', "'") and value[-1] == value[0]

