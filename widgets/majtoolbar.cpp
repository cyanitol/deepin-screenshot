#include "majtoolbar.h"
#include "utils/baseutils.h"
#include "bigcolorbutton.h"
#include "toolbutton.h"

#include <QApplication>
#include <QButtonGroup>
#include <QDebug>
#include <QCursor>

namespace {
    const int TOOLBAR_HEIGHT = 28;
    const int TOOLBAR_WIDTH = 284;
    const int BUTTON_SPACING = 3;
}
MajToolBar::MajToolBar(QWidget *parent)
    : QLabel(parent),
      m_isChecked(false)
{
    initWidgets();
}

MajToolBar::~MajToolBar() {}

void MajToolBar::initWidgets() {
    setStyleSheet(getFileContent(":/resources/qss/majtoolbar.qss"));
    setFixedSize(TOOLBAR_WIDTH, TOOLBAR_HEIGHT);
    setFocusPolicy(Qt::StrongFocus);
    setMouseTracking(true);
    setAcceptDrops(true);
    installEventFilter(this);

    QButtonGroup* buttonGroup = new QButtonGroup(this);
    buttonGroup->setExclusive(true);
    ToolButton* rectBtn = new ToolButton();
    rectBtn->setObjectName("RectBtn");
    buttonGroup->addButton(rectBtn);
    ToolButton* ovalBtn = new ToolButton();
    ovalBtn->setObjectName("OvalBtn");
    buttonGroup->addButton(ovalBtn);
    ToolButton* arrowBtn = new ToolButton();
    arrowBtn->setObjectName("ArrowBtn");
    buttonGroup->addButton(arrowBtn);
    ToolButton* penBtn = new ToolButton();
    penBtn->setObjectName("PenBtn");
    buttonGroup->addButton(penBtn);
    ToolButton* textBtn = new ToolButton();
    textBtn->setObjectName("TextBtn");
    buttonGroup->addButton(textBtn);
    BigColorButton* colorBtn = new BigColorButton();
    colorBtn->setObjectName("ColorBtn");
    buttonGroup->addButton(colorBtn);
    ToolButton* saveBtn = new ToolButton();
    saveBtn->setObjectName("SaveBtn");
    saveBtn->setFixedSize(15, 22);
    buttonGroup->addButton(saveBtn);
    ToolButton* saveListBtn = new ToolButton();
    saveListBtn->setObjectName("ListBtn");
    saveListBtn->setFixedSize(10, 22);
    buttonGroup->addButton(saveListBtn);
    ToolButton* shareBtn = new ToolButton();
    shareBtn->setObjectName("ShareBtn");
    buttonGroup->addButton(shareBtn);
    ToolButton* closeBtn = new ToolButton();
    closeBtn->setObjectName("CloseBtn");
    buttonGroup->addButton(closeBtn);

    m_baseLayout = new QHBoxLayout();
    m_baseLayout->setMargin(0);
    m_baseLayout->addSpacing(4);
    m_baseLayout->addWidget(rectBtn);
    m_baseLayout->addSpacing(BUTTON_SPACING);
    m_baseLayout->addWidget(ovalBtn);
    m_baseLayout->addSpacing(BUTTON_SPACING);
    m_baseLayout->addWidget(arrowBtn);
    m_baseLayout->addSpacing(BUTTON_SPACING);
    m_baseLayout->addWidget(penBtn);
    m_baseLayout->addSpacing(BUTTON_SPACING);
    m_baseLayout->addWidget(textBtn);
    m_baseLayout->addSpacing(BUTTON_SPACING);
    m_baseLayout->addWidget(colorBtn);
    m_baseLayout->addSpacing(BUTTON_SPACING);
    m_baseLayout->addWidget(saveBtn);
    m_baseLayout->addSpacing(0);
    m_baseLayout->addWidget(saveListBtn);
    m_baseLayout->addSpacing(BUTTON_SPACING);
    m_baseLayout->addWidget(shareBtn);
    m_baseLayout->addSpacing(BUTTON_SPACING);
    m_baseLayout->addWidget(closeBtn);
    m_baseLayout->addSpacing(4);
    m_baseLayout->addStretch();

    setLayout(m_baseLayout);

    connect(rectBtn, &ToolButton::clicked, this, [=](){
        m_isChecked = !m_isChecked;
        emit buttonChecked(m_isChecked, "rectangle");
    });
    connect(ovalBtn, &ToolButton::clicked, this, [=](){
        m_isChecked = !m_isChecked;
        emit buttonChecked(m_isChecked, "Oval");
    });
    connect(arrowBtn, &ToolButton::clicked, this, [=](){
                m_isChecked = !m_isChecked;
        emit buttonChecked(m_isChecked, "Arrow");
    });
    connect(penBtn, &ToolButton::clicked, this, [=](){
                m_isChecked = !m_isChecked;
        emit buttonChecked(m_isChecked, "Pen");
    });
    connect(textBtn, &ToolButton::clicked, this, [=](){
                m_isChecked = !m_isChecked;
        emit buttonChecked(m_isChecked, "Text");
    });
    connect(colorBtn, &ToolButton::clicked, this, [=](){
                m_isChecked = !m_isChecked;
        emit buttonChecked(m_isChecked, "Color");
    });
    connect(saveBtn, &ToolButton::clicked, this, [=](){
                m_isChecked = !m_isChecked;
        emit buttonChecked(m_isChecked, "Save");
    });
    connect(saveListBtn, &ToolButton::clicked, this, [=](){
        m_isChecked = !m_isChecked;
        emit buttonChecked(m_isChecked, "SaveList");
    });

    connect(closeBtn, &ToolButton::clicked, this, [=](bool checked){
        Q_UNUSED(checked);
        qDebug() << "screenshot will exit!";
        qApp->quit();
    });
}

bool MajToolBar::isButtonChecked() {
    return m_isChecked;
}

bool MajToolBar::eventFilter(QObject *watched, QEvent *event) {
    Q_UNUSED(watched);

    if (event->type() == QEvent::Enter) {
        setCursor(Qt::ArrowCursor);
        qApp->setOverrideCursor(Qt::ArrowCursor);
    }
    return false;
}

void MajToolBar::mouseMoveEvent(QMouseEvent *ev) {
    Q_UNUSED(ev);
    qApp->setOverrideCursor(Qt::ArrowCursor);
}